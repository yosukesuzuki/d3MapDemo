# -*- coding: utf-8 -*-
"""
adminapp.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""
import logging
import json
import werkzeug
import re
import datetime
import time
RE_REMOVE_HTTP = re.compile(ur'^http:')
from werkzeug import Response

from google.appengine.api import files
from google.appengine.api import memcache
from google.appengine.api import search
from google.appengine.ext import db 
from google.appengine.ext import blobstore
from google.appengine.ext import deferred
from google.appengine.api.images import get_serving_url

from kay import utils
from kay.utils import render_to_response
from kay.utils import url_for
from kay.utils.paginator import Paginator, InvalidPage, EmptyPage
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from kay.handlers import blobstore_handlers

from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS,MODEL_DICT,get_page_content
from mainapp.models import AdminPage,BlobStoreImage,Article
from adminapp.forms import AdminPageForm
from adminapp.utils import construct_datetime_from_string,construct_image_json_from_content

def index(request):
    admin_page_list = [{'title':_('Page Manager'),'info':AdminPage.__doc__,'url':'/admin/adminpage/list'},
            {'title':_('Article Manager'),'info':Article.__doc__,'url':'/admin/article/list'},
            {'title':_('Image Manager'),'info':BlobStoreImage.__doc__,'url':'/admin/image/manager/'}]
    return render_to_response('adminapp/index.html', {'admin_page_list': admin_page_list})

def flush_memcache(request):
    memcache.flush_all()
    return Response('success')

def update_page_order(request):
    try:
        new_orders = request.form['orders']
    except:
        return Response('Error:no data')
    new_orders_list = new_orders.split(';')
    new_order_incre = 0
    for new_order in new_orders_list:
        if new_order is None or new_order == '':
            continue
        new_order_entity = db.get(new_order) 
        if new_order_entity:
            new_order_entity.page_order = new_order_incre 
            new_order_incre += 1
            new_order_entity.put()
    memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
    return Response('Success:new order was saved,'+str(new_order_incre)+' times')

def add_translation(request,parent_key):
    if request.method != 'POST':
        return Response('POST method is required')
    parent_entity = db.get(parent_key)
    if parent_entity is None:
        return Response('Default lang entity is not found')
    model_name = parent_entity.kind()
    try:
        title = request.form['title']
    except:
        return Response('Title is required')
    trans_key_name = parent_entity.key().name()+'_'+request.form['lang']
    trans_entity = MODEL_DICT[model_name](parent=parent_entity,key_name=trans_key_name,title=title)
    for k in request.form:
        if k in ['title','url']:
            continue
        logging.info(k)
        logging.info(request.form[k])
        try:
            setattr(trans_entity,k,request.form[k])
        except:
            if request.form[k] == 'on' or request.form[k] == 'true':
                setattr(trans_entity,k,True)
            else:
                setattr(trans_entity,k,False)
        #custom process for tags_string
        #if k == 'tags_string':
        #    #logging.info(request.form[k].split(','))
        #    setattr(trans_entity,'tags',request.form[k].split(','))
        if k == 'content':
            #logging.info(request.form[k].split(','))
            images = construct_image_json_from_content(request.form[k])
            setattr(trans_entity,'images',images)
    trans_entity.put()
    children = MODEL_DICT[model_name].all().ancestor(parent_entity).fetch(1000)
    for child in children:
        if child.lang == request.form['lang']:
            deferred.defer(index_full_text_search,child.key())
    return Response('Success:add transltion')

def get_children(request,parent_key):
    parent_entity = db.get(parent_key)
    children = MODEL_DICT[parent_entity.kind()].all().ancestor(parent_entity.key()).fetch(1000)
    return_list = []
    for child in children:
        logging.info(u'title:'+child.title)
        if parent_key != str(child.key()):
            return_list.append(str(child.key()))
    return Response(u';'.join(return_list))

def preview(request,entity_key):
    '''
    preview page
    '''
    browser_lang = request.lang
    entity = db.get(entity_key)
    model_name = entity.kind()
    key_name = entity.key().name()
    page = get_page_content(browser_lang,model_name,key_name,True)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    page.title = '('+_('Preview')+')'+page.title
    sidebar = {'sidebar_title':_('Link'),'sidebar_list':[{'title':_('About'),'url':'/about/'},{'title':_('Contact'),'url':'/contact/'}]}
    return render_to_response('mainapp/show_each_page.html', {'page': page,'model_name':model_name,'sidebar':sidebar})

def create_search_document(key):
    entity = db.get(key)
    timestamp = int(time.mktime((entity.update).timetuple()))
    title = entity.title
    content = entity.content
    lang = entity.lang
    display_page_flg = str(entity.display_page_flg)
    model_name = entity.kind()
    try:
        parent = str(entity.parent().key())
    except:
        parent = ''
    url = entity.external_url
    if url is None or url == '':
        try:
            key_name = entity.parent().key().name()
        except:
            key_name = entity.key().name()
        if model_name == 'AdminPage':
            url = url_for('mainapp/show_each_page',key_name=key_name)
        else:
            url = url_for('mainapp/show_each_article',key_name=key_name)
    return search.Document(doc_id=entity.kind()+'_'+entity.key().name(),
            fields=[search.TextField(name='title', value=title, language=lang),
                search.TextField(name='content', value=content, language=lang),
                search.TextField(name='key', value=str(key), language='en'),
                search.TextField(name='model_name', value=model_name, language=lang),
                search.TextField(name='display_page_flg', value=display_page_flg, language='en'),
                search.TextField(name='lang', value=lang, language=lang),
                search.TextField(name='images', value=entity.images, language=lang),
                search.TextField(name='url', value=url, language='en'),
                search.TextField(name='parent', value=parent, language='en'),
                search.NumberField(name='timestamp', value=timestamp)])

def index_full_text_search(key):
    entity = db.get(key) 
    document = create_search_document(entity.key())
    try:
        search.Index(name='Pages').put(document)
        return True
    except search.Error:
        return False

def index_full_text_search_by_key_name(model_name,key_name):
    entity = MODEL_DICT[model_name].get_by_key_name(key_name)
    index_full_text_search(entity.key())
    return True

def image_manager(request):
    #TODO add image search function by full text search
    return render_to_response('adminapp/image_manager.html', {'title':_('Image manager')})

def image_upload_url(request):
    upload_url = blobstore.create_upload_url(url_for('adminapp/upload_handler'))
    return Response('"'+upload_url+'"',mimetype='application/json')

def image_list_json(request):
    #TODO duplication,I have to DRY below code
    blob_info_query = blobstore.BlobInfo.all().order('-creation')
    blob_info_results = blob_info_query.fetch(10)
    for r in blob_info_results:
        bsi_entity = BlobStoreImage.get_by_key_name(r.md5_hash)
        if bsi_entity is None:
            bsi_entity = BlobStoreImage(key_name=r.md5_hash,file_name=r.filename,blob_key=r.key())
            bsi_entity.put()
    query = BlobStoreImage.all().order('-update')
    paginator = Paginator(query,10)
    try:
        page = int(request.args.get('page','1'))
    except ValueError:
        page = 1
    try:
        results = paginator.page(page)
    except (EmptyPage,InvalidPage):
        results = paginator.page(paginator.num_pages)
    return_list = []
    for r in results.object_list:
        if r.image_path is None or r.image_path == '':
            r.image_path = get_serving_url(r.blob_key.key())
            r.put()
        return_list.append({'key':str(r.key()),
            'id':r.key().name(),
            'title':r.title,
            'file_name':r.file_name,
            'note':r.note,
            'image_path':RE_REMOVE_HTTP.sub('',r.image_path),
            'update':str(r.update)[:16]})
    return Response(json.dumps({'images':return_list,
        'current_page':results.number,
        'total_pages':results.paginator.num_pages}, ensure_ascii=False))
    
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        query = blobstore.BlobInfo.all().order('-creation')
        results = query.fetch(1000)
        for r in results:
            bsi_entity = BlobStoreImage.get_by_key_name(r.md5_hash)
            if bsi_entity is None:
                bsi_entity = BlobStoreImage(key_name=r.md5_hash,file_name=r.filename,blob_key=r.key())
                bsi_entity.put()
        headers = {} 
        return werkzeug.Response('success', headers=headers, status=200)

def image_delete(request,key):
    bsi_entity = BlobStoreImage.get(key)
    bsi_entity.blob_key.delete()
    bsi_entity.delete()
    return Response('success')

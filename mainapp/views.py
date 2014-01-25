# -*- coding: utf-8 -*-
"""
mainapp.views
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
import datetime
import urllib
from werkzeug import Response,redirect

from google.appengine.api import files
from google.appengine.api import memcache
from google.appengine.api import search

from django.utils import html
from django.utils import feedgenerator

from kay.utils import render_to_response
from kay.utils import get_by_key_name_or_404
from kay.utils import url_for 
from kay.utils.paginator import Paginator, InvalidPage, EmptyPage
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from settings import DEFAULT_LANG

from mainapp.markdown2 import markdown
from mainapp.models import AdminPage,BlobStoreImage,Article

'''
global vars
'''
TOP_PAGE_CONTENT_NUM = 4
CACHE_NAME_FOR_TOP_PAGE_RESULTS = 'top-page-contents'
DUMMY_DATA_FOR_TOP_PAGE = [{'title':'Dummy,first title','snippet':'this is dummy snippet','url':'/first/'},
        {'title':'Dummy,second title','snippet':'this is dummy snippet','url':'/second/'},
        {'title':'Dummy,third title','snippet':'this is dummy snippet','url':'/third/'},
        {'title':'Dummy,fourth title','snippet':'this is dummy snippet','url':'/fourth/'}]
MODEL_DICT = {'AdminPage':AdminPage,'BlobStoreImage':BlobStoreImage,'Article':Article}

def index(request):
    '''
    top page
    '''
    browser_lang = request.lang
    results = memcache.get(CACHE_NAME_FOR_TOP_PAGE_RESULTS+'-'+browser_lang)
    if results is None:
        query_results = AdminPage.all().filter(u'lang =',DEFAULT_LANG).filter(u'display_page_flg =',True).order('page_order').fetch(limit=TOP_PAGE_CONTENT_NUM)
        results = []
        for r in query_results:
            if browser_lang != DEFAULT_LANG:
                translations = AdminPage.all().ancestor(r.key()).fetch(1000)
                browser_lang_trans = None
                for trans in translations:
                    if trans.lang == browser_lang:
                        browser_lang_trans = trans
                        break
                if browser_lang_trans:
                    r.content = browser_lang_trans.content
                    r.title = browser_lang_trans.title
            url = r.external_url if r.external_url else '/'+r.key().name()+'/'
            if browser_lang != DEFAULT_LANG:
                url += '?hl='+browser_lang
            snippet = html.strip_tags(markdown(r.content)).split('\n')[0]
            try:
                first_image = json.loads(r.images)['images'][0]['image_path']
            except:
                first_image = None
            results.append({'title':r.title,'snippet':snippet,'url':url,'first_image':first_image})
        if len(results) == 0:results = DUMMY_DATA_FOR_TOP_PAGE
        logging.info(results)
        memcache.set(CACHE_NAME_FOR_TOP_PAGE_RESULTS+'-'+browser_lang,results)
    article_results = get_article_list(browser_lang,1,4)
    return render_to_response('mainapp/index.html', {'results': results,'article_results':article_results})

def show_each_page(request,key_name):
    '''
    each page
    '''
    browser_lang = request.lang
    try:
        prior_lang = request.args['hl']
    except:
        prior_lang = None
    if prior_lang and browser_lang != prior_lang:
        browser_lang = prior_lang
    model_name = 'AdminPage'
    page = get_page_content(browser_lang,model_name,key_name)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    sidebar = {'sidebar_title':_('Link'),'sidebar_list':[{'title':_('About'),'url':'/about/'},{'title':_('Contact'),'url':'/contact/'}]}
    return render_to_response('mainapp/show_each_page.html', {'page': page,'model_name':model_name,'sidebar':sidebar})

def get_page_content(browser_lang,model_name,key_name,is_admin=False):
    default_page = MODEL_DICT[model_name].get_by_key_name(key_name)
    if default_page is None:
        return None 
    return_page = default_page
    if is_admin is False and default_page.display_page_flg is False:
        return None 
    if browser_lang != DEFAULT_LANG:
        logging.info('browser_lang:'+browser_lang)
        translations = MODEL_DICT[model_name].all().ancestor(default_page.key()).fetch(1000)
        for trans in translations:
            if trans.lang == browser_lang:
                return_page = trans
                if hasattr(default_page,'display_time'):
                    return_page.display_time = default_page.display_time
    markdown_converted_content = markdown(return_page.content)
    snippet = html.strip_tags(markdown_converted_content).split('\n')[0]
    return_page.content = markdown_converted_content
    setattr(return_page,'snippet',snippet)
    try:
        first_image = json.loads(return_page.images)['images'][0]['image_path']
    except:
        first_image = None
    setattr(return_page,'first_image',first_image)
    return return_page

def article_list(request):
    browser_lang = request.lang
    article_per_page = 10 
    try:
        page = int(request.args.get('page','1'))
    except ValueError:
        page = 1
    article_results = get_article_list(browser_lang,page,article_per_page)
    return render_to_response('mainapp/article_list.html', {'article_results':article_results})

def show_each_article(request,key_name):
    browser_lang = request.lang
    try:
        prior_lang = request.args['hl']
    except:
        prior_lang = None
    if prior_lang and browser_lang != prior_lang:
        browser_lang = prior_lang
    model_name = 'Article'
    page = get_page_content(browser_lang,model_name,key_name)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    results_dic = get_article_list(browser_lang,1,10)
    sidebar = {'sidebar_title':_('Back number'),'sidebar_list':results_dic['articles']}
    return render_to_response('mainapp/show_each_page.html', {'page': page,'model_name':model_name,'sidebar':sidebar})

def get_article_list(browser_lang,page,article_per_page,tag_name=False):
    if tag_name:
        tag_name_encoded = unicode(tag_name)
    else:
        tag_name_encoded = str(tag_name)
    memcache_key = u'article-'+str(page)+u'-'+str(article_per_page)+u'-'+urllib.quote(tag_name_encoded.encode('utf-8'))+u'-'+browser_lang
    logging.info(memcache_key)
    results_dic = memcache.get(memcache_key)
    #if memcache data exist return
    if results_dic:
        return results_dic
    #else memcach data is none,query from datastore
    now = datetime.datetime.now()
    logging.info(now)
    query = Article.all().filter(u'lang =',DEFAULT_LANG).filter(u'display_page_flg =',True)
    if tag_name:
        query.filter(u'tags =',tag_name)
    query.filter(u'display_time <',now).order('-display_time')
    paginator = Paginator(query,article_per_page)
    try:
        results = paginator.page(page)
    except (EmptyPage,InvalidPage):
        results = paginator.page(paginator.num_pages)
    return_list = []
    for r in results.object_list:
        browser_lang_trans = None
        if browser_lang != DEFAULT_LANG:
            translations = Article.all().ancestor(r.key()).fetch(1000)
            #browser_lang_trans = None
            for trans in translations:
                if trans.lang == browser_lang:
                    browser_lang_trans = trans
                    break
            if browser_lang_trans:
                r.content = browser_lang_trans.content
                r.title = browser_lang_trans.title
        url = r.external_url if r.external_url else url_for('mainapp/show_each_article',key_name=r.key().name())
        if browser_lang_trans and browser_lang != DEFAULT_LANG:
            url += '?hl='+browser_lang
        snippet = html.strip_tags(markdown(r.content)).split('\n')[0]
        try:
            first_image = json.loads(r.images)['images'][0]['image_path']
        except:
            first_image = None
        return_list.append({'key':str(r.key()),
            'id':r.key().name(),
            'title':r.title,
            'snippet':snippet,
            'url':url,
            'first_image':first_image,
            'display_time':str(r.display_time)[:16]})
    results_dic = {'articles':return_list,
    'current_page':results.number,
    'previous_page':results.previous_page_number,
    'next_page':results.next_page_number,
    'has_next':results.has_next,
    'total_pages':results.paginator.num_pages,
    'tag_name':tag_name}
    memcache.set(memcache_key,results_dic)
    return results_dic 

def search_by_tag(request,tag_name):
    browser_lang = request.lang
    article_per_page = 10
    try:
        page = int(request.args.get('page','1'))
    except ValueError:
        page = 1
    article_results = get_article_list(browser_lang,page,article_per_page,tag_name)
    return render_to_response('mainapp/article_list.html', {'article_results':article_results})

def search_by_keyword(request):
    browser_lang = request.lang
    try:
        keyword = request.args['keyword']
        if keyword == '':
            return redirect(url_for('mainapp/bad_request',message_code='keywordrequired001'))
    except:
        return redirect(url_for('mainapp/bad_request',message_code='keywordrequired001'))
    try:
        page = int(request.args['page'])
    except:
        page = 1
    try:
        cursor_string = request.args['cursor']
    except:
        cursor_string = None
    article_per_page = 10
    try:
        article_results = get_search_list(keyword,browser_lang,page,article_per_page,cursor_string)
    except:
        return redirect(url_for('mainapp/bad_request',message_code='error001'))

    #return Response(json.dumps(article_results, ensure_ascii=False))
    return render_to_response('mainapp/article_list.html', {'article_results':article_results})

def bad_request(request):
    return render_to_response('mainapp/bad_request.html', {})

def get_search_list(keyword,browser_lang,page,article_per_page,cursor_string=None):
    limit = article_per_page 
    timestamp_desc = search.SortExpression(
            expression='timestamp',
            direction=search.SortExpression.DESCENDING,
            default_value=0)
    sort = search.SortOptions(expressions=[timestamp_desc], limit=1000)
    if cursor_string is None:
        cursor = search.Cursor()
    else:
        cursor = search.Cursor(web_safe_string=cursor_string)
    options = search.QueryOptions(
            limit=limit,  # the number of results to return
            cursor=cursor,
            sort_options=sort)
    if browser_lang == 'all':
        query_string = keyword +' display_page_flg:True'
    else:
        query_string = keyword +' lang:'+browser_lang+' display_page_flg:True'
    query = search.Query(query_string=query_string,options=options)
    index = search.Index(name='Pages')
    si_results = index.search(query)
    next_cursor_obj = si_results.cursor
    logging.info(next_cursor_obj)
    logging.info(si_results.number_found)
    if next_cursor_obj:
        next_cursor = next_cursor_obj.web_safe_string
    else:
        next_cursor = None
    return_list = []
    for sr in si_results:
        title = None
        snippet = None
        url = None
        first_image = None
        display_time = None
        key = None
        for f in sr.fields:
            if f.name == 'content': 
                snippet = html.strip_tags(markdown(f.value)).split('\n')[0]
            elif f.name == 'images':
                try:
                    first_image = json.loads(f.value)['images'][0]['image_path']
                except:
                    pass
            elif f.name == 'title':
                title = f.value
            elif f.name == 'key':
                key = f.value
            elif f.name == 'url':
                url = f.value
        if browser_lang != DEFAULT_LANG:
            if url:
                url += '?hl='+browser_lang
        return_list.append({'key':key,
            'id':sr.doc_id,
            'title':title,
            'snippet':snippet,
            'url':url,
            'first_image':first_image,
            'display_time':display_time})
    results_dic = {'articles':return_list,
    'current_page':page,
    'total_pages':si_results.number_found/article_per_page+1,
    'tag_name':None,
    'cursor':next_cursor,
    'keyword':keyword}
    return results_dic

def rss_feed(request):
    browser_lang = request.lang
    feed = feedgenerator.Rss201rev2Feed(
            title = _('RSS feed for Kaybootstrap'),
            link = request.url,
            description = _('feed for kaybootstrap'),
            language = browser_lang)
    article_results = get_article_list(browser_lang,1,10)
    for a in article_results['articles']:
        feed.add_item(
                title = a['title'],
                link = 'http://'+request.host+a['url'],
                description=a['snippet'])
    rss = feed.writeString("utf-8")
    return Response(rss, mimetype='text/xml')

def site_map(request):
    #TODO return sitemap xml for search engine crawler
    return Response('Under construction')

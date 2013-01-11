# -*- coding: utf-8 -*-
# adminapp.urls
# 
import urllib

from google.appengine.api import memcache
from kay.routing import (
  ViewGroup, Rule
)
from kay.generics import crud
from kay.generics import admin_required

from adminapp.forms import AdminPageForm
from mainapp.models import AdminPage
from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS

class AdminPageCRUDViewGroup(crud.CRUDViewGroup):
     model = AdminPage
     form = AdminPageForm
     templates = {
             'show':'adminapp/general_show.html',
             'list':'adminapp/general_list.html',
             'update':'adminapp/general_update.html',
             }
     def get_query(self, request):
         return self.model.all().order('page_order')
     def get_additional_context_on_update(self, request, form):
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
         return {}
     def get_additional_context_on_create(self, request, form):
         key_name = None
         url = None
         try:
             url = request.form['url']
         except:
             pass
         if url:
             key_name = url
         else:
             key_name = urllib.quote(request.form['title'])
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
         return {'key_name':key_name}
     authorize = admin_required

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='adminapp.views.index'),
    Rule('/update/page/order/', endpoint='update_page_order', view='adminapp.views.update_page_order'),
  ),
  AdminPageCRUDViewGroup(),
]


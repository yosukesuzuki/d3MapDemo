# -*- coding: utf-8 -*-
# mainapp.models

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images

from kay.auth.models import GoogleUser
from kay.i18n import gettext as _
# Create your models here.

class AdminTopPage(db.Model):
    '''
    Model for top page setting.
    If admin set Url field, url is set as key name or escaped Title String is set as key name
    '''
    title = db.StringProperty(verbose_name=_('Title'),required=True)
    display_page_flg = db.BooleanProperty(verbose_name=_('Display a page or hidden'),default=False)
    page_order = db.IntegerProperty(verbose_name=_('Page order on top page'),default=99999)
    snippet = db.TextProperty(verbose_name=_('Snippet'))
    content = db.TextProperty(verbose_name=_('Content'))
    url = db.StringProperty(verbose_name=_('Url,page identifier of this content,only at first time'))
    external_url = db.StringProperty(verbose_name=_('External Url,If link to an outside page,optional'))
    images = db.TextProperty(verbose_name=_('Images,JSON Format'))
    image_layout = db.StringProperty(verbose_name=_('Image Layout Setting'),choices=('auto','manual'),default='auto')
    show_image_on_top_flg = db.BooleanProperty(verbose_name=_('Show the first image on top page'),default=True)
    update = db.DateTimeProperty(verbose_name=_('Update'),auto_now=True)
    created = db.DateTimeProperty(verbose_name=_('Created'),auto_now_add=True)

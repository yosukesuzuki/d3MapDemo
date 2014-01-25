# -*- coding: utf-8 -*-

'''
original template filters by kaybootstrap
'''
import datetime
from kay.i18n import gettext as _

def toMarkdown(text):
    from mainapp.markdown2 import markdown
    return_html = markdown(text) 
    return return_html

def enforceMinus9hours(datetime_string):
    display_time = datetime.datetime.strptime(datetime_string,'%Y-%m-%d %H:%M')
    display_time = display_time + datetime.timedelta(hours = -9)
    return_datetime_string = display_time.strftime('%Y-%m-%d %H:%M')
    return return_datetime_string

MESSAGES = {'default':_('Invalid Parameter'),
        'loginfail001':_('Login Failed'),
        'loginsuccess001':_('Login Success'),
        'logoutsuccess001':_(u'Logout Success'),
        'keywordrequired001':_('Keyword required'),
        'error001':_('Error')}

def returnMessage(message_code):
    try:
        message = MESSAGES[message_code]
    except:
        message = MESSAGES[message_code]
    return message

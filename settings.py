# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'UTC'
DEBUG = True
PROFILE = False
SECRET_KEY = 'ReplaceItWithSecretString'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = True
DEFAULT_LANG = 'en'

MIDDLEWARE_CLASSES = (
        'kay.auth.middleware.AuthenticationMiddleware',
        'kay.sessions.middleware.SessionMiddleware',
        'kay.utils.flash.FlashMiddleware',
        'kay.ext.appstats.middleware.AppStatsMiddleware',
)

INSTALLED_APPS = (
        'kay.auth',
        'kay.i18n',
        'mainapp',
        'adminapp',
)

APP_MOUNT_POINTS = {
        'mainapp':'/',
        'adminapp':'/admin',
}

# You can remove following settings if unnecessary.
CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
  'mainapp.context_processors.default_lang',
  'mainapp.context_processors.lang_list',
)

JINJA2_FILTERS = {
    'toMarkdown':'mainapp.template_filters.toMarkdown',
    'enforceMinus9hours':'mainapp.template_filters.enforceMinus9hours',
    'returnMessage':'mainapp.template_filters.returnMessage',
}

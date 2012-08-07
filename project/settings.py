# -*- encoding: utf-8 -*-

import os
import socket
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as \
        DEFAULT_TEMPLATE_CONTEXT_PROCESSORS

# Rapports d'erreurs
SERVER_EMAIL = 'ne-pas-repondre@auf.org'
EMAIL_SUBJECT_PREFIX = '[ECM - %s] ' % socket.gethostname()
ADMINS = (
    ('Équipe ARI-SI', 'developpeurs@ca.auf.org'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

LANGUAGE_CODE = 'fr-ca'

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'sitestatic')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'mptt',
    'ecm',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

SOUTH_TESTS_MIGRATE = False

ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

ECM_VIEWS_SETTINGS = ('project.ecm.views_settings', )

from conf import *

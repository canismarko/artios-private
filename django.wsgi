import os
import sys

sys.path.append('/home/mark/artios_privatesite')
sys.path.append('/home/mark')

os.environ['PYTHON_EGG_CACHE'] = '/home/mark/artios_privatesite/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

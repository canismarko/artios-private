import os
import sys

sys.path.append('/srv/artiosprivate')
# sys.path.append('/home/mark')

os.environ['PYTHON_EGG_CACHE'] = '/srv/artiosprivate/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

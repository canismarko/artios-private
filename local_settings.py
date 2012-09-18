# This is the local settings file. It is generally ignored by git
# so it provibes settings useful for this specific deployement.
# The example settings below tweak the settings for a
# basic production server. 

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Administrator', 'webmaster@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'artios_privatesite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

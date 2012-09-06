# -*- coding: utf-8 -*-
"""
Django settings for toby project.

This is the version for development environnment only. For production usage you should 
create a new settings file like "prod_settings.py" where you import these settings and 
overwrite the required ones like WEBAPP_ROOT, ADMINS, DATABASES, SECRET_KEY (important), 
EMAIL, etc..
"""
import os

#####
#
#   1. Database, email server, etc.. settings
#
#####

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'tobyweb',                      # Or path to database file if using sqlite3.
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'USER': 'tobyweb',                      # Not used with sqlite3.
        'PASSWORD': 'tobyweb',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+v&6a#!j6g03wdbw+$g-8_vg4=7wuv0vq+=82&)$r27o3t9nw7'

#####
#
#   2. Paths resolutions
#
#####

# Define the webapp absolute path
# In production this must be defined manually
WEBAPP_ROOT = os.path.abspath(os.path.dirname(__file__))

# Medias directory name
MEDIA_DIRNAME = 'medias'

# Static directory name
STATIC_DIRNAME = 'static'

# URL that handles the media served from ``MEDIA_ROOT``. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# Si vous utilisez une URL pour cette option, il faudra alors spécifier manuellement 
# en dur la valeur de ``MEDIA_ROOT``
MEDIA_URL = '/{0}/'.format(MEDIA_DIRNAME)
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(WEBAPP_ROOT, MEDIA_DIRNAME)+"/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/{0}/'.format(STATIC_DIRNAME)
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(WEBAPP_ROOT, STATIC_DIRNAME)+"/"

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(WEBAPP_ROOT, 'webapp_statics/'),
)

# URL prefix for admin media -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = os.path.join('/', STATIC_DIRNAME, 'admin/')

# Absolute paths to your template directories
TEMPLATE_DIRS = (
    os.path.join(WEBAPP_ROOT, 'templates/'),
)


#####
#
#   3. Apps linking and further
#
#####

# For debug_toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar_user_panel.panels.UserPanel',
    #'inserdiag_webapp.utils.debugtoolbar_filter.InserdiagVersionDebugPanel',
    #'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.signals.SignalDebugPanel',
    #'debug_toolbar.panels.logger.LoggingPanel',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    #'homeapps.utils.site_metas',
    #'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'tobyweb.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #'debug_toolbar',
    #'autobreadcrumbs',
    'tribune',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

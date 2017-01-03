"""
Django settings for vkusotiiki project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from .base_settings import *
import dj_database_url


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {'default': dj_database_url.config()}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dn0#iyk_ct_@_c0o=u%%ow0^i=1-!&+d^6r_31sp4tf&r*f2%0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
# DJANGO_SETTINGS_MODULE = 'vkusotiiki.settings.live_settings'
# print(DJANGO_SETTINGS_MODULE)
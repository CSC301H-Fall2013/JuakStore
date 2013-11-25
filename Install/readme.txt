==== JuakStore Installation ====

Required:
    Python 2.7
    Django 1.5
    python-dateutil
    juakstore
    Apache (if deploying on server)

======= Basic Setup ========

1. Installing Python:
First make sure that you have python 2.7 installed on your computer. To do so type "python" in your console. 
If you have python installed, then type:

import sys
sys.version

If you do not have python installed, download it from http://www.python.org/download/

2. Installing Pip:
Check if you have pip installed by typing `pip` into a console.
If you do not have pip installed do so by following the instructions here: 
http://www.pip-installer.org/en/latest/installing.html#using-the-installer


3. Installing Django:
The next step depends on which operating system you are using:
Unix/Mac: type `sudo pip install Django`
Windows: Open a command shell with administrative rights and type `pip install Django`

3. Install python-dateutil:
This is a package used by juakstore, to install it type:
`pip install python-dateutil`

4. Install juakstore:
Change to the directory where juakstore is located and type:
`pip install --user juakstore-1.0.tar.gz`

5. Setting up Django project:
In the directory you would like to create your Django project type:
`django-admin.py startproject <name of project>`
Where <name of project> is replaced with what you would like to name your project
 
=============================

======Setting up Juakstore =============

=====
Juakstore
=====

Juakstore is a client booking application made for the East Scarborough Storefront.

Detailed documentation is in the "docs" directory.

Quick start
-----------


==== Modify settings.py for steps 1-6==== 

1. Add "juakstore" and "registration" to your INSTALLED_APPS and enable "django.contrib.admin" like this:

      INSTALLED_APPS = (
          ...
          'django.contrib.admin',
          'juakstore',
          'juakstore.juakregister',
      )

2. Add the following settings to setup the email, where the EMAIL settings will need to be changed based on your email account:

ACCOUNT_ACTIVATION_DAYS = 365

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'eaststorefront@gmail.com'
EMAIL_HOST_PASSWORD = 'JuakfrontPassword1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

3. Add `import os` to the top of the file.

4. Add os.path.join(PROJECT_DIR, 'static') to your STATICFILES_DIRS:

    STATICFILES_DIRS = (
        ...
        os.path.join(PROJECT_DIR, 'static'),
    )

5. Set STATIC_URL = '/static/'

6. Setup your database in the DATABASES setting
    Note: you will need to create a database yourself if not using sqlite3

7. Add the following to urls.py:
    
    ...
    from django.conf.urls import patterns, include, url
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    admin.autodiscover()
    
    urlpatterns = patterns('',
        ...
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('juakstore.urls', namespace='juakstore')),
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
        url(r'^accounts/', include('juakstore.juakregister.backends.default.urls')),
    )

8. Run `python manage.py syncdb` to create the juakstore models.

9.  Running the app would depend on how you would like to deploy it:

    a) If deploying on an Apache Server, change:
     WSGIScriptAlias to be the path to wsgi.py in the project
        Example: if your project is named Storefront then the path would be to Storefront/Storefront/wsgi.py
     WSGIPythonPath to be the path to the root of the project
        Example: if your project is named Storefront then the path would be to Storefront/
     <Directory> to be the path to the project
        Example: if your project is named Storefront the the path would be to Storefront/Storefront
     Then run `sudo apachectl restart` to restart the apache server
    
    
    b) If you would like to run this server locally:
        Run `python manage.py runserver` and navigate to localhost.
"""
WSGI config for usakag_fashions_modified_v1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys
# add the usakag_fashions_modified_v1 path into the sys.path
sys.path.append('<PATH_TO_MY_DJANGO_PROJECT>/usakag_fashions_modified_v1')

# add the virtualenv site-packages path to the sys.path
sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')

# poiting to the project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'usakag_fashions_modified_v1.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

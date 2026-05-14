"""
WSGI config for spa_booking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

"""
WSGI config for spa_booking project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Thêm đoạn này để Render không bị lỗi khi thiếu thư viện C của MySQL
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spa_booking.settings')

application = get_wsgi_application()
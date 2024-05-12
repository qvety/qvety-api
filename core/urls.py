from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from qt_search.api import app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', app.urls),
]

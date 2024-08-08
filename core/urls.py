from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from core.api import ninja

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', ninja.urls),
]

if settings.DEBUG and settings.ALLOW_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

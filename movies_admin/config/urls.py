from django.contrib import admin
from django.urls import include, path

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(path('debug/', include('debug_toolbar.urls')))

# -*- coding: utf-8 -*-

from django.urls import include, path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_app/', include('test_project.test_app.urls')),
]


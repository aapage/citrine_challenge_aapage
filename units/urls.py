from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^si/$', unit_converter, name='unit_converter'),
]

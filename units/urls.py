from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^si/$', test_view, name='test_view'),
]

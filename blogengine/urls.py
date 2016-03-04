from django.conf.urls import url
from django.views.generic import ListView
from blogengine.models import Story

urlpatterns = [
    url(r'story$', ListView.as_view(model=Story)),
    ]
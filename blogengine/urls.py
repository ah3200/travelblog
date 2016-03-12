from django.conf.urls import url
from django.views.generic import ListView, DetailView
from blogengine.models import Story

urlpatterns = [
    url(r'^(?P<page>\d+)?/?$', ListView.as_view(model=Story, paginate_by=2)),
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Story,
        )),
    ]
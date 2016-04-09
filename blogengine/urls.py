from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from blogengine.models import Story, Category, Tag
from blogengine.views import CategoryListView, TagListView, StoriesFeed, CategoryStoriesFeed, TagStoriesFeed
from blogengine import views

urlpatterns = [
    url(r'^story/(?P<page>\d+)?/?$', ListView.as_view(model=Story, paginate_by=2)),
    url(r'^story/(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Story,
        )),
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/(?P<page>\d+)?/?$', CategoryListView.as_view(model=Category, paginate_by=2)),
    url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/(?P<page>\d+)?/?$', TagListView.as_view(model=Tag, paginate_by=2), name='tag-view'),
    # Post RSS feed
    url(r'^feeds/stories/$', StoriesFeed()),
    # Category RSS feed
    url(r'^feeds/stories/category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryStoriesFeed()),
    # Tag RSS feed
    url(r'^feeds/stories/tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagStoriesFeed()),
    # Search stories
    url(r'^search', views.getSearchResults),
    url(r'^story/new/$', views.createNewStory),
    url(r'^api/', include('api.urls')),
    ]
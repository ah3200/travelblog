from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^$', views.story_list, name='story-list'),
    url(r'^(?P<pk>\d+)$', views.story_detail, name='story-detail'),
    ]
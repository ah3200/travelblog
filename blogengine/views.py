from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from blogengine.models import Category, Story

# Create your views here.
class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Story.objects.filter(category=category)
        except Category.DoesNotExist:
            return Story.objects.none()
            
class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except:
            return Story.objects.none()
            
class StoriesFeed(Feed):
    title = "RSS Feed - stories"
    link = "feeds/stories/"
    description = "RSS feed - blog post"
    
    def items(self):
        return Story.objects.order_by('-pub_date')
        
    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.text
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from blogengine.models import Category, Story, Tag
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown2

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
        extras = ["fenced-code-blocks"]
        content = mark_safe(markdown2.markdown(force_unicode(item.text), extras=extras))
        return content
        
class CategoryStoriesFeed(StoriesFeed):
    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)
        
    def title(self, obj):
        return "RSS feed - stories in category %s" % obj.name
        
    def link(self, obj):
        return obj.get_absolute_url()
        
    def description(self, obj):
        return "RSS feed - stories in category %s" % obj.name
        
    def items(self, obj):
        return Story.objects.filter(category=obj).order_by('-pub_date')
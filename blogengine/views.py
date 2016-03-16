from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.syndication.views import Feed
from blogengine.models import Category, Story, Tag
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown2

# Create your views here.
class CategoryListView(ListView):
    
    template_name = 'blogengine/category_story_list.html'
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Story.objects.filter(category=category)
        except Category.DoesNotExist:
            return Story.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        try:
            context['category'] = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            context['category'] = None
        return context
    
class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.story_set.all()
        except:
            return Story.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        try:
            context['tag'] = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            context['tag'] = None
        return context
        
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
        
class TagStoriesFeed(StoriesFeed):
    def get_object(self, request, slug):
        return get_object_or_404(Tag, slug=slug)
        
    def title(self, obj):
        return "RSS feed - stories with tagged %s" % obj.name
        
    def link(self, obj):
        return obj.get_absolute_url()
        
    def description(self, obj):
        return "RSS feed - stories with tagged %s" % obj.name
        
    def items(self, obj):
        try:
            tag = Tag.objects.get(slug=obj.slug)
            return tag.story_set.all()
        except Tag.DoesNotExist:
            return Story.objects.none()

def getSearchResults(request):
    # Get query data
    query = request.GET.get('q','')
    page = request.GET.get('page',1)
    
    # Query the database
    if query:
        results = Story.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
    else:
        results = None
    
     # Add pagination
    pages = Paginator(results, 2)
    
    # Get specified page
    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)
        
    # Display the search results
    return render_to_response('blogengine/search_story_list.html',
                             {'page_obj': returned_page,
                              'object_list': returned_page.object_list,
                              'search': query})
                               
    
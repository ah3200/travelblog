from django.shortcuts import render
from django.views.generic import ListView
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
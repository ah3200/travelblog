from django.contrib import admin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
import models

class StoryAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Story,StoryAdmin)


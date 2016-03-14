from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
import models

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(models.Category)
admin.site.register(models.Story,StoryAdmin)


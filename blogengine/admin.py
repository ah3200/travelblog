from django.contrib import admin

# Register your models here.
from blogengine.models import Story 

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

admin.site.register(Story,StoryAdmin)

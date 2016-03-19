from django import forms
from blogengine.models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'text', 'slug', 'category')
    #title = forms.CharField(label='Title', max_length=200)
    #text = forms.CharField(widget=forms.Textarea, label='Story')
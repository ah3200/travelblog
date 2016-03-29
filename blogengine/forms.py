from django import forms
from blogengine.models import Story
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'text', 'slug', 'category',)
        widgets = {
            'text': SummernoteInplaceWidget()
        }
#        widgets = {
#            'text': forms.fields.TextInput(attrs={
#                'placeholder': 'Enter your story here',
#                'class': 'form-control input-lg',
#            }),
#        }
#        error_messages = {
#            'text': {'required': EMPTY_ITEM_ERROR}
#        }
    #title = forms.CharField(label='Title', max_length=200)
    #text = forms.CharField(widget=forms.Textarea, label='Story')
# from dataclasses import field
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'enctype': 'multipart/form-data'})

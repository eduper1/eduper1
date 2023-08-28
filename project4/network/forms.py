from django import forms
from django.forms import fields
from .models import Post

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {
            'content': ('New Post'),
        }
        help_texts = {
            'content': ('Express your idea freely...'),
        }
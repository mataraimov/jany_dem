from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['username', 'age', 'diagnose', 'treatment', 'target', 'photo', 'description', 'balance']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

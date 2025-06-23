# forms.py
from django import forms
from .models import PolicyComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = PolicyComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2}),
        }

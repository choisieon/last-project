from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # 글 제목, 내용만 입력받음


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

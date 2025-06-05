from django import forms
from .models import Post, PostImage, Comment
from tinymce.widgets import TinyMCE

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PostForm(forms.ModelForm):
    images = MultipleFileField(  # ✅ MultipleFileField 사용
        required=False,
        label="이미지 업로드 (최대 2개)"
    )
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']  # 글 제목, 내용만 입력받음
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),   # 드롭다운(select)에도 클래스 적용
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


    # 추가된 부분: __init__ 메서드 (카테고리 초기값에 따라 TinyMCE 적용)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('category') == 'review':
            self.fields['content'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})

    # 추가된 부분: 이미지 개수 검증
    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 2:
            raise forms.ValidationError("최대 2개까지 업로드 가능합니다.")
        return images

# 기존 ImageForm과 CommentForm은 그대로 유지
class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Comment
        fields = ['content']

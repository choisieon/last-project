import re
from django import forms
from .models import Post, PostImage, Comment
from tinymce.widgets import TinyMCE
from taggit_autosuggest.widgets import TagAutoSuggest


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
    images = MultipleFileField(
        required=False,
        label="이미지 업로드 (최대 2개)"
    )

    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'thumbnail', 'images', 'tags']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'rows': 10, 'required': False}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'tags': TagAutoSuggest('taggit.tag'),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        thumbnail = cleaned_data.get('thumbnail')
        # 후기글일 때 썸네일 필수 검증
        if category == 'review' and not thumbnail:
            self.add_error('thumbnail', '후기글은 썸네일 이미지가 필수입니다.')
        return cleaned_data
    
    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 2:
            raise forms.ValidationError("최대 2개까지 업로드 가능합니다.")
        return images

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if isinstance(tags, str) and tags.strip().startswith('['):
            try:
                tag_list = [item['value'] for item in json.loads(tags)]
                return ','.join(tag_list)  # 쉼표로 구분된 문자열로 변환
            except Exception:
                return tags  # 파싱 실패 시 원본 반환
        return tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # ManyToMany 필드 저장
        return instance


# 기타 폼 (CommentForm, ImageForm 등은 그대로 유지)
class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Comment
        fields = ['content']

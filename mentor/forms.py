from django import forms
from django.apps import apps
from .models import Question, Answer, MentorRequest, UserProfile  # 여기 OK

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'title', 'content', 'is_anonymous']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class OnboardingForm(forms.ModelForm):
    concerns = forms.ModelMultipleChoiceField(
        queryset=apps.get_model('accounts', 'Concern').objects.all(),  # ✅ 요기
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['role', 'concerns', 'keywords']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class MentorRequestForm(forms.ModelForm):
    class Meta:
        model = MentorRequest
        fields = ['category', 'message']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class UserProfileForm(forms.ModelForm):
    concerns = forms.ModelMultipleChoiceField(
        queryset=apps.get_model('accounts', 'Concern').objects.all(),  # ✅ 요기도
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['role', 'concerns', 'keywords']
        widgets = {
            'role': forms.RadioSelect(choices=[
                ('mentor', '나는 멘토'), 
                ('mentee', '나는 멘티'), 
                ('both', '둘다')
            ]),
            'concerns': forms.CheckboxSelectMultiple,
            'keywords': forms.TextInput(attrs={'placeholder': '예: mbti, 대학생, 00학과, 인생설계, 자취러'}),
        }

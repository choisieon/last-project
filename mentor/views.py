from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, UserProfile, MentorRequest
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, MentorRequestForm, UserProfileForm
from django.db.models import Count

def index(request):
    return render(request, 'community/index.html')


def mentor_home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'mentor/mentor_home.html', {'questions': questions})


def question_list(request):
    sort = request.GET.get('sort', 'latest')

    # 모든 질문에 답변 수를 계산
    questions = Question.objects.annotate(answer_count=Count('answers'))

    # 정렬 기준에 따라 질문 목록 정렬
    if sort == 'views':
        questions = questions.order_by('-views')
    elif sort == 'likes':
        questions = questions.order_by('-likes')
    elif sort == 'answers':
        questions = questions.order_by('-answer_count')  # 답변 수 기준 정렬
    else:  # default: latest
        questions = questions.order_by('-created_at')

    return render(request, 'mentor/question_list.html', {
        'questions': questions,
        'sort': sort
    })

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.views += 1
    question.save()
    answers = question.answers.all().order_by('created_at')
    return render(request, 'mentor/question_detail.html', {
        'question': question,
        'answers': answers
    })


@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            try:
                profile = request.user.mentor_profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=request.user, nickname=request.user.username)
            question.author = profile
            question.created_at = timezone.now()
            question.save()
            return redirect('mentor:question_list')
    else:
        form = QuestionForm()
    return render(request, 'mentor/question_form.html', {'form': form})


@login_required
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user.mentor_profile
            answer.save()
            return redirect('mentor:question_detail', question_id)
    else:
        form = AnswerForm()

    return render(request, 'mentor/answer_form.html', {'form': form, 'question': question})


@login_required
def mentor_request(request, mentor_id=None):
    if request.method == 'POST':
        form = MentorRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            try:
                profile = request.user.mentor_profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=request.user, nickname=request.user.username)
            req.mentee = profile
            req.created_at = timezone.now()
            if mentor_id:
                req.mentor = get_object_or_404(UserProfile, id=mentor_id)
            req.save()
            return redirect('mentor:question_list')
    else:
        form = MentorRequestForm()
    return render(request, 'mentor/mentor_request_form.html', {'form': form})


def mentor_list(request):
    mentors = UserProfile.objects.filter(is_mentor=True)
    return render(request, 'mentor/mentor_list.html', {'mentors': mentors})


def mentor_profile(request, mentor_id):
    mentor = get_object_or_404(UserProfile, id=mentor_id, is_mentor=True)
    return render(request, 'mentor/mentor_profile.html', {'mentor': mentor})


@login_required
def onboarding(request):
    profile = request.user.mentor_profile  # mentor_profile는 related_name임
    if profile.onboarding_complete:
        return redirect('mentor:mentor_home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_complete = True
            profile.save()
            form.save_m2m()
            return redirect('mentor:mentor_home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'mentor/onboarding.html', {'form': form})

@login_required
def onboarding(request):
    # 프로필이 없으면 자동 생성
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.onboarding_complete:
        return redirect('mentor:mentor_home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_complete = True
            profile.save()
            form.save_m2m()
            return redirect('mentor:mentor_home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'mentor/onboarding.html', {'form': form})

@login_required
def mentor_list(request):
    mentors = UserProfile.objects.filter(is_mentor=True)
    return render(request, 'mentor/mentor_list.html', {'mentors': mentors})


def mentor_profile(request, userprofile_id):
    mentor = get_object_or_404(UserProfile, id=userprofile_id)
    return render(request, 'mentor/mentor_profile.html', {'mentor': mentor})

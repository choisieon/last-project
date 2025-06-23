from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, UserProfile, MentorRequest, Message
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, MentorRequestForm, UserProfileForm
from django.db.models import Count
from django.db.models import Prefetch
from .models import ChatRoom, ChatMessage  # ChatRoom이 정의된 곳에서 import
from django.http import HttpResponseForbidden, JsonResponse
from .models import Comment
from django.db.models import F
from django.views.decorators.http import require_POST
from datetime import date
from .models import Question
from django.http import JsonResponse
from datetime import timedelta                 # ✅ 1시간 전 계산용
from .models import Question, QuestionView     # ✅ 모델



CATEGORY_MAP = {
    'all': '전체',
    'life': '🌱 인생선배',
    'college': '🏫 대학선배',
    'love': '💘 연애선배',
    'house': '🏠 자취선배',
    'job': '💼 취업선배',
    'money': '💳 지갑선배',
    'fitness': '💪 운동선배',
    'etc': '📌 기타',
}

def index(request):
    return render(request, 'community/index.html')

def mentor_home(request):
    sort = request.GET.get('sort', 'latest')
    questions = Question.objects.annotate(answer_count=Count('answers'))

    cat = request.GET.get('category', 'all')
    if cat != 'all':
        questions = questions.filter(category=cat)

    if sort == 'views':
        questions = questions.order_by('-views')
    elif sort == 'likes':
        questions = questions.order_by('-likes')
    elif sort == 'answers':
        questions = questions.order_by('-answer_count')
    else:
        questions = questions.order_by('-created_at')

    return render(request, 'mentor/mentor_home.html', {
        'questions': questions,
        'sort': sort,
        'current_category': cat,
        'categories': CATEGORY_MAP,
    })


def question_list(request):
    sort = request.GET.get('sort', 'latest')
    questions = Question.objects.annotate(answer_count=Count('answers'))

    cat = request.GET.get('category', 'all')
    # 🔍 항상 찍히도록 바깥에 두기
    print("🧩 DEBUG border → cat:", repr(cat), "| before filter count:", questions.count())

    if cat != 'all':
        questions = questions.filter(category=cat)
        print("🧩 DEBUG after filter count:", questions.count())

    # 정렬 로직...

    return render(request, 'mentor/question_list.html', {
        'questions': questions,
        'sort': sort,
        'current_category': cat,
        'categories': CATEGORY_MAP,
    })

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'GET':
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recently_viewed = QuestionView.objects.filter(
            question=question,
            user=request.user,
            viewed_at__gte=one_hour_ago
        ).exists()

        if not recently_viewed:
            QuestionView.objects.create(question=question, user=request.user, viewed_at=timezone.now())
            question.views += 1
            question.save()

    answers = question.answers.all().order_by('created_at')
    return render(request, 'mentor/question_detail.html', {
        'question': question,
        'answers': answers,
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

            # ✅ 내공 +5점
            profile.points += 5
            profile.save()
            return redirect('mentor:mentor_home')
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
            answer.author = request.user.profile
            answer.save()
            return redirect('mentor:question_detail', question_id)
    else:
        form = AnswerForm()

    # ✅ 여기 return 추가
    return render(request, 'mentor/answer_form.html', {
        'form': form,
        'question': question,
    })



from django.utils import timezone
from django.contrib import messages

@login_required
def mentor_request(request, mentor_id=None, question_id=None):
    if request.method == 'POST':
        form = MentorRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            req.mentee = profile
            req.created_at = timezone.now()

            if mentor_id:
                req.mentor = get_object_or_404(UserProfile, id=mentor_id)
            if question_id:
                req.question = get_object_or_404(Question, id=question_id)

            req.save()

            # ✅ 내공 +20점 (멘티에게)
            profile.points += 20
            profile.save()

            return redirect('mentor:question_list')
    else:
        form = MentorRequestForm()
    return render(request, 'mentor/mentor_request_form.html', {'form': form})




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


@login_required
def mentor_request_direct(request, mentor_id):
    question_id = request.GET.get('question_id') or request.POST.get('question_id')

    if request.method == 'POST':
        form = MentorRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            req.mentee = profile
            req.mentor = get_object_or_404(UserProfile, id=mentor_id)
            req.created_at = timezone.now()

            if question_id:
                req.question = get_object_or_404(Question, id=question_id)

            req.save()

            # ✅ 내공 +20점 (멘티에게)
            profile.points += 20
            profile.save()

            if question_id:
                return redirect('mentor:question_detail', pk=question_id)
            else:
                return redirect('mentor:mentor_home')
    else:
        form = MentorRequestForm()

    return render(request, 'mentor/mentor_request_form.html', {'form': form})


@login_required
def mentor_requests_received(request):
    profile = request.user.mentor_profile  # 현재 로그인한 사용자의 프로필

    requests = MentorRequest.objects.filter(mentor=profile).order_by('-created_at')

    return render(request, 'mentor/request_received.html', {
        'requests': requests
    })

@login_required
def accept_mentor_request(request, request_id):
    mentor_request = get_object_or_404(MentorRequest, id=request_id)

    if request.user != mentor_request.mentor.user:
        return redirect('mentor:mentor_home')  # 보안용

    # 수락 처리
    mentor_request.is_accepted = True
    mentor_request.save()

    # ✅ 내공 +20점 (멘토에게)
    mentor_request.mentor.points += 20
    mentor_request.mentor.save()

    # ChatRoom 생성 (존재하지 않으면)
    try:
        mentor_request.chatroom
    except ChatRoom.DoesNotExist:
        ChatRoom.objects.create(mentor_request=mentor_request)

    # ✅ advice_center로 이동 (네임스페이스 고려)
    return redirect('advice:advice_center')  # ← advice 앱에 네임스페이스가 있다면
    # return redirect('/advice/center/')     # ← 네임스페이스 없다면 하드코딩으로도 가능




@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    messages = list(ChatMessage.objects.filter(room=room).order_by('timestamp'))

    # 각 메시지에 show_sender 속성 추가
    for i, msg in enumerate(messages):
        if i == 0 or msg.sender != messages[i - 1].sender:
            msg.show_sender = True
        else:
            msg.show_sender = False

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ChatMessage.objects.create(
                room=room,
                sender=request.user.mentor_profile,
                content=content
            )
        return redirect('mentor:chat_room', room_id=room.id)

    return render(request, 'mentor/chat_room.html', {
        'room': room,
        'chatroom' : room,
        'messages': messages
    })




# questions = Question.objects.all().prefetch_related(
#     Prefetch('answers', queryset=Answer.objects.order_by('created_at'))
# )

# for q in questions:
#     q.first_answer = q.answers.first()

@login_required
def my_chat_rooms(request):
    profile = request.user.mentor_profile
    rooms = ChatRoom.objects.filter(mentor_request__mentee=profile)
    return render(request, 'mentor/my_chat_rooms.html', {'rooms': rooms})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author.user != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
    if request.method == 'POST':
        question.delete()
        return redirect('mentor:mentor_home')  # 삭제 후 홈으로 이동
    return render(request, 'mentor/confirm_delete.html', {'object': question, 'type': '질문'})

@login_required
def answer_delete(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.author.user != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
    if request.method == 'POST':
        answer.delete()
        return redirect('mentor:question_detail', pk=answer.question.pk)
    return render(request, 'mentor/confirm_delete.html', {'object': answer, 'type': '답변'})

@login_required
def delete_chatroom(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    # 현재 사용자가 채팅방에 참여한 사람인지 확인
    if request.user.mentor_profile != room.user1 and request.user.mentor_profile != room.user2:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    room.delete()
    return redirect('mentor:mentor_home')  # 삭제 후 이동할 경로 (원하는 곳으로 수정 가능)


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id)

    # 메시지를 보낸 사람만 삭제 가능
    if request.user.mentor_profile != message.sender:
        return HttpResponseForbidden("삭제 권한이 없습니다.")

    room_id = message.room.id
    message.delete()

    return redirect('mentor:chat_room', room_id=room_id)

@login_required
def comment_create(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            Comment.objects.create(
                answer=answer,
                author=request.user.profile,
                content=content
            )
            # ✅ 내공 +3점
            request.user.profile.points += 3
            request.user.profile.save()

    return redirect('mentor:question_detail', pk=answer.question.pk)


@require_POST
@login_required
def question_like(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user

    if user in question.likes.all():
        question.likes.remove(user)
    else:
        question.likes.add(user)

    return redirect('mentor:question_detail', pk=pk)

@require_POST
@login_required
def question_curious(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user

    if user in question.curious.all():
        question.curious.remove(user)
    else:
        question.curious.add(user)

    return redirect('mentor:question_detail', pk=pk)


@login_required
@require_POST
def toggle_like(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user in question.likes.all():
        question.likes.remove(request.user)
        liked = False
    else:
        question.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': question.likes.count()})



@login_required
def delete_mentor_request(request, request_id):
    req = get_object_or_404(MentorRequest, id=request_id)

    # 로그인한 사용자가 신청자(멘티)거나 수신자(멘토)인 경우만 삭제 허용
    user_profile = request.user.mentor_profile
    if req.mentee == user_profile or req.mentor == user_profile:
        req.delete()

    return redirect('advice:advice_center')  # 'advice_center'가 advice 앱의 URL name이라면 이렇게

@login_required
def delete_selected_chatrooms(request):
    if request.method == 'POST':
        room_ids = request.POST.getlist('delete_rooms')
        for room_id in room_ids:
            room = get_object_or_404(ChatRoom, id=room_id)
            if room.mentor_request.mentee.user == request.user or room.mentor_request.mentor.user == request.user:
                room.delete()
    return redirect('advice:advice_center')

@login_required
def delete_chatrooms(request):
    if request.method == 'POST':
        room_ids = request.POST.getlist('delete_rooms')
        for room_id in room_ids:
            room = get_object_or_404(ChatRoom, id=room_id)

            # 채팅방에 연결된 mentor_request도 함께 삭제
            mentor_request = getattr(room, 'mentor_request', None)
            if mentor_request:
                mentor_request.delete()

            # 채팅방 삭제
            room.delete()

    return redirect('advice:advice_center')


@login_required
def answer_adopt(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.question.author.user:
        if answer.is_adopted:
            # 이미 채택된 상태 → 취소
            answer.is_adopted = False
            answer.author.points -= 20
        else:
            # 아직 채택 안 됨 → 채택
            answer.is_adopted = True
            answer.author.points += 20

        answer.author.save()
        answer.save()

    return redirect('mentor:question_detail', pk=answer.question.pk)

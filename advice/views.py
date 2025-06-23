from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # ← 이 줄 추가!!!
from mentor.models import MentorRequest, ChatRoom
from accounts.models import UserProfile



@login_required
def advice_center(request):
    profile = request.user.mentor_profile
    sent_requests = MentorRequest.objects.filter(mentee=profile).order_by('-created_at')
    received_requests = MentorRequest.objects.filter(mentor=profile).order_by('-created_at')
    chat_rooms = ChatRoom.objects.filter(
        Q(mentor_request__mentee=profile) | Q(mentor_request__mentor=profile)
    ).order_by('-created_at')

    return render(request, 'advice.html', {
     'sent_requests': sent_requests,
    'received_requests': received_requests,
    'chat_rooms': chat_rooms,
})
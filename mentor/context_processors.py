# mentor/context_processors.py
from .models import MentorRequest

def mentor_notifications(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.mentor_profile
            requests = MentorRequest.objects.filter(mentor=profile)
            return {'mentor_requests': requests}
        except:
            return {'mentor_requests': []}
    return {'mentor_requests': []}

from django.shortcuts import render, get_object_or_404
from .models import YouthPolicy

# Create your views here.
def basic_page(request):
    policies = YouthPolicy.objects.all()
    return render(request, 'basic_page.html', {'policies': policies})

def youth_policy_detail(request, policy_id):
    policy = get_object_or_404(YouthPolicy, id=policy_id)
    return render(request, 'youth_policies.html', {'policy': policy})
from django.shortcuts import render

# Create your views here.

def mentor_home(request):
    return render(request, 'mentor/mentor_home.html')
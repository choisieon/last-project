# chungsulmo/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'community/index.html')
    # 또는 다른 템플릿, 또는 리다이렉트도 가능
    # return redirect('post_list')

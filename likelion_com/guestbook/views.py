from django.http import HttpResponseRedirect
from django.shortcuts import render
from guestbook.models import Guestbook
from accounts.models import Profile
from django.contrib.auth.models import User

# Create your views here.

def write(request):
    guestbook = Guestbook()
    guestbook.content = request.POST['content']
    guestbook = Guestbook.objects.create(content=guestbook.content, author=request.user)
    guestbook.save()
    return HttpResponseRedirect('list')

def delete(id):
    guestbook = Guestbook.objects.get(id=id)
    guestbook.delete() 

    return HttpResponseRedirect('list')

def list(request):
    guestbooklist = Guestbook.objects.all().order_by('-created_at')
    return render(request, 'guestbook/list.html', {'guestbooklist': guestbooklist})
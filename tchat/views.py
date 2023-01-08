from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = 'Invalid username or password'

    template = loader.get_template('login.html')
    context = {
        'error': error
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def channels_new(request):
    template = loader.get_template('channels_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def channels_view(request, channel_id):
    template = loader.get_template('channels_view.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def channels_settings(request, channel_id):
    template = loader.get_template('channels_settings.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def channels_messages(request, channel_id):
    return JsonResponse({'channel_id':channel_id})

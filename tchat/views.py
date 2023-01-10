from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .models import Channel, Message, Membership

@login_required
def index(request):
    memberships = Membership.objects.filter(user=request.user)

    template = loader.get_template('index.html')
    context = {
        'memberships': memberships
    }
    return HttpResponse(template.render(context, request))

def account_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = 'Invalid username or password'

    template = loader.get_template('account.html')
    context = {
        'page': 'login',
        'error': error
    }
    return HttpResponse(template.render(context, request))

def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('/')
        except:
            error = 'Username or email already taken'

    template = loader.get_template('account.html')
    context = {
        'page': 'register',
        'error': error
    }
    return HttpResponse(template.render(context, request))

def account_logout(request):
    logout(request)
    return redirect('/')

@login_required
def channels_new(request):
    if request.method == 'POST':
        name = request.POST['name']
        logo = 'https://via.placeholder.com/150' # TODO: upload logo
        channel = Channel(name=name, logo=logo, created=timezone.now())
        channel.save()
        membership = Membership(user=request.user, channel=channel, role='owner', last_read=timezone.now())
        membership.save()
        return redirect('/channels/%d/' % channel.id)

    template = loader.get_template('channels_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def channels_view(request, channel_id):
    Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    template = loader.get_template('index.html')
    context = {
        'channel': {
            'id': channel.id,
            'name': channel.name,
            'logo': channel.logo
        }
    }
    return HttpResponse(template.render(context, request))

@login_required
def channels_settings(request, channel_id):
    Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    template = loader.get_template('channels_settings.html')
    context = {
        'channel': {
            'id': channel.id,
            'name': channel.name,
            'logo': channel.logo
        }
    }
    return HttpResponse(template.render(context, request))

@login_required
def channels_messages(request, channel_id, page=1):
    Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    if request.method == 'POST':
        content = request.POST['content']
        message = Message(user=request.user, channel=channel, content=content, published=timezone.now())
        message.save()

    messages = Message.objects.filter(channel=channel).order_by('-published')[(page-1)*10:(page)*10]
    
    return JsonResponse({
        'channel': {
            'id': channel.id,
            'name': channel.name,
            'logo': channel.logo
        },
        'messages': [
            {
                'id': message.id,
                'user': {
                    'id': message.user.id,
                    'username': message.user.username,
                    'me': message.user.id == request.user.id
                },
                'content': message.content,
                'published': message.published
            }
            for message in messages
        ]
    })

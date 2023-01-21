from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .models import Channel, Message, Membership

# List of emojis to display in the emoji keyboard
# (so that we don't hardcode them in the template)
emojis = [
    '😀', '😘', '😭', '❤️', '😂', '😋', '😉', '😎', '😡', '😱', '😴', '🤔', '😏', '🤣',
    '🤩', '🤪', '🤯', '🤬', '🤮', '🤢', '😵', '🤧', '🥵', '🥶', '🥴', '🤠', '🤡', '🍆'
]

@login_required
def index(request):
    # Get conversations for authenticated user
    # sorted by last message published
    memberships = (Membership.objects
        .filter(user=request.user)
        .annotate(last_message=(Max('channel__message__published')))
        .order_by('-last_message'))

    template = loader.get_template('index.html')
    context = {
        'memberships': memberships
    }
    return HttpResponse(template.render(context, request))

def account_login(request):
    # In case user is already logged in
    # redirect to home page
    if request.user.is_authenticated:
        return redirect('/')
    
    error = None
    if request.method == 'POST':
        # Handle a POST request
        # ie. user is trying to login
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
    # In case user is already logged in
    # redirect to home page
    if request.user.is_authenticated:
        return redirect('/')
    
    error = None
    if request.method == 'POST':
        # Handle a POST request
        # ie. user is trying to register
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)

            defaultChannel = Channel.objects.filter(name='General').first()
            if defaultChannel is not None:
                membership = Membership(user=user, channel=defaultChannel, role='member', last_read=timezone.now())
                membership.save()

            return redirect('/')
        except:
            # The create_user failed, so we know that the username
            # or email already exists (else it shouldn't fail)
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
def channels(request):
    if request.method == 'POST':
        # Handle a POST request
        # ie. user is trying to create a new channel
        name = request.POST['name']
        logo = 'https://via.placeholder.com/150' # TODO: upload logo
        channel = Channel(name=name, logo=logo, created=timezone.now())
        channel.save()
        membership = Membership(user=request.user, channel=channel, role='owner', last_read=timezone.now())
        membership.save()

    # Get conversations for authenticated user
    # sorted by last message published
    memberships = (Membership.objects
        .filter(user=request.user)
        .annotate(last_message=(Max('channel__message__published')))
        .order_by('-last_message'))

    # The difference here, compared to the index view,
    # is that we return a JSON response instead of a template
    return JsonResponse({
        'channels': [
            {
                'id': membership.channel.id,
                'name': membership.channel.name,
                'logo': membership.channel.logo
            }
            for membership in memberships
        ]
    })
    
@login_required
def channels_view(request, channel_id):
    # Get the channel and the membership for the authenticated user
    membership = Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)
    
    if request.method == 'DELETE':
        # Handle a DELETE request
        # ie. user is trying to leave or delete the channel
        if membership.role == 'owner':
            # If the user is the owner of the channel,
            # delete the channel (and all its users and messages)
            channel.delete()
        else :
            # If the user is not the owner of the channel,
            # just leave the channel
            membership.delete()
        return JsonResponse({})

    if request.method == 'POST':
        # Handle a POST request
        # ie. user is trying to update the channel
        # We don't use PUT because Django doesn't decode
        # the body of PUT requests, which is sad
        channel.name = request.POST['name']
        channel.save()
        return JsonResponse({})
        
    template = loader.get_template('index.html')
    context = {
        'channel': channel,
        'membership': membership,
        'emojis': emojis
    }
    return HttpResponse(template.render(context, request))

@login_required
def channels_settings(request, channel_id):
    # Get the channel and the membership for the authenticated user
    membership = Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    # We also need to get all the users that are not in the channel
    # so that we can add them (in the select field)
    users = User.objects.exclude(id__in=[ membership.user.id for membership in channel.membership_set.all() ])
    
    template = loader.get_template('index.html')
    context = {
        'channel': channel,
        'membership': membership,
        'users': users,
        'settings': True
    }
    return HttpResponse(template.render(context, request))

@login_required
def channels_messages(request, channel_id, page=1):
    # Get the channel and the membership for the authenticated user
    membership = Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    if request.method == 'POST':
        # Handle a POST request
        # ie. user is trying to create a new message
        # or update an existing message (if an id is provided)
        content = request.POST['content']
        message_id = request.POST['message_id']
        if message_id != -1 and message_id != '-1':
            # Id provided, update the message
            message = Message.objects.get(id=message_id, channel=channel_id)
            message.content = content
            message.save()
        else:
            # No id provided, create a new message
            message = Message(user=request.user, channel=channel, content=content, published=timezone.now())
            message.save()

    if request.method == 'DELETE':
        # Handle a DELETE request
        # ie. user is trying to delete a message
        message_id = page
        message = Message.objects.get(id=message_id, channel=channel_id)
        message.delete()
        return JsonResponse({})

    messages = Message.objects.filter(channel=channel).order_by('-published')[(page-1)*10:(page)*10]
    
    # Return the messages as JSON
    # so that we can use them in JavaScript (with Ajax)
    return JsonResponse({
        'channel': {
            'id': channel.id,
            'name': channel.name,
            'logo': channel.logo,
            'membership': {
                'role': membership.role,
            }
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

@login_required
def channels_users(request, channel_id, user_id=None):
    # Get the channel and the membership for the authenticated user
    Membership.objects.get(user=request.user, channel=channel_id)
    channel = Channel.objects.get(id=channel_id)

    if request.method == 'POST':
        # Handle a POST request
        if user_id is None:
            # If no user id is provided, add the user to the channel
            user_id = request.POST['user']
            user = User.objects.get(id=user_id)
            membership = Membership(user=user, channel=channel, role='member', last_read=timezone.now())
            membership.save()
        else:
            # If a user id is provided, update the user's membership
            # (for now only role can be updated)
            role = request.POST['role']
            membership = Membership.objects.get(user=user_id, channel=channel_id)
            membership.role = role
            membership.save()
    
    if request.method == 'DELETE' and user_id is not None:
        # Handle a DELETE request
        # ie. user is trying to remove a user from the channel
        membership = Membership.objects.get(user=user_id, channel=channel_id)
        membership.delete()

    # Return the users as JSON
    return JsonResponse({
        'users': [
            {
                'id': membership.user.id,
                'username': membership.user.username,
                'role': membership.role
            }
            for membership in channel.membership_set.all()
        ]
    })

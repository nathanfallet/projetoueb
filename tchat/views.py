from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def register(request):
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def channels_new(request):
    template = loader.get_template('channels_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

def channels_view(request, channel_id):
    template = loader.get_template('channels_view.html')
    context = {}
    return HttpResponse(template.render(context, request))

def channels_settings(request, channel_id):
    template = loader.get_template('channels_settings.html')
    context = {}
    return HttpResponse(template.render(context, request))

def channels_messages(request, channel_id):
    return JsonResponse({'channel_id':channel_id})

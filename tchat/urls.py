from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.account_login, name='login'),
    path('logout/', views.account_logout, name='logout'),
    path('register/', views.account_register, name='register'),
    path('channels/new/', views.channels_new, name='channels_new'),
    path('channels/<int:channel_id>/', views.channels_view, name='channels_view'),
    path('channels/<int:channel_id>/settings/', views.channels_settings, name='channels_settings'),
    path('channels/<int:channel_id>/messages/', views.channels_messages, name='channels_messages'),
    path('channels/<int:channel_id>/messages/<int:page>', views.channels_messages, name='channels_messages'),
    path('channels/<int:channel_id>/users/', views.channels_users, name='channels_users'),
]

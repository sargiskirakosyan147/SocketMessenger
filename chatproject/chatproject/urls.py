from django.urls import path, include
from onlinechat.views import join_chat

urlpatterns = [
    path('', join_chat, name='home'),
    path('chat/', include('onlinechat.urls')),
]

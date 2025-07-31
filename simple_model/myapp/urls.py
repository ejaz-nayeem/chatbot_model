# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('startchat/', views.start_chat),
    path('startchat/<int:id>/add_singlechat/', views.add_singlechat),
    path('chatcontent/<int:conv_id>/', views.chatcontent),
    path('chatlist/', views.chatlist),
]

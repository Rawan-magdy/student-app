from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_chat, name='ai_chat'),
    path('<int:pk>/', views.ai_chat, name='ai_conversation'),
    path('<int:pk>/delete/', views.conversation_delete, name='conversation_delete'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index ,name = 'index'),
    path('speech-to-text/', views.speech_to_text, name='speech-to-text'),
    path('set-language/', views.set_language, name='set-language'),
    path('text-to-speech/', views.text_to_speech, name='text-to-speech'),
    ]

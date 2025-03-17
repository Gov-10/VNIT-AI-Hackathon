from django.urls import path
from .views import home, chatbot_response, contact_us,event_detail,event_list,register
urlpatterns = [
    path("", home, name="home"),  # Home page
    path("chatbot_response/", chatbot_response, name="chatbot_response"),
    path('contact_us/',contact_us, name="contact_us"),
     path('event/<slug:slug>/', event_detail, name='event_detail'),
     path('events/', event_list, name='event_list'),
     path('register/', register,name="register" )
]
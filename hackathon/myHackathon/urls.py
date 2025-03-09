from django.urls import path
from .views import home, chatbot_response

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("chatbot_response/", chatbot_response, name="chatbot_response"),
]

from django.urls import path
from .views import home, chatbot_response, algorithmia, web_weave, contact_us
urlpatterns = [
    path("", home, name="home"),  # Home page
    path("chatbot_response/", chatbot_response, name="chatbot_response"),
    path('algorithmia/',algorithmia, name="algorithmia"),
    path('web_weave/',web_weave, name="web_weave"),
    path('contact_us/',contact_us, name="contact_us")
]
from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
import os  # To manage API keys securely

def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message")  
        api_key = os.getenv("AI_API_KEY")  # Store API Key in environment variables
        
        # Example: Fetch response from OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "gpt-4", "messages": [{"role": "user", "content": user_input}]}
        )
        
        return JsonResponse(response.json())  



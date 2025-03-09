from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
import json  
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from dotenv import load_dotenv

def home(request):
    return render(request, "home.html")  # Render a simple home page



load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": message}]}]
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            api_response = response.json()

            # DEBUG: Print the response for debugging
            print("API Response:", api_response)

            if "candidates" in api_response:
                reply = api_response["candidates"][0]["content"]["parts"][0]["text"]
                return JsonResponse({"reply": reply})
            else:
                return JsonResponse({"reply": "Error: No valid response from Gemini API."})
        
        except Exception as e:
            return JsonResponse({"reply": f"API error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request method."})

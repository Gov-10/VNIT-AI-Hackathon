from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
import json  
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rapidfuzz import process  # Import fuzzy matching
from .models import Event  # Import Event model

def home(request):
    return render(request, "home.html")  

def algorithmia(request):
    return render(request, 'algorithmia.html') 

def web_weave(request):
    return render(request, 'web_weave.html')

def contact_us(request):
    return render(request, 'contact_us.html')

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Define allowed AI-related questions
ALLOWED_QUESTIONS = [
    "hello",
    "hi",
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What is the future of robotics?",
    "What is the impact of AI on jobs?",
    "What are some futuristic technologies?",
    "What is quantum computing?",
    "What are the latest trends in AI?",
    "Tell me about NIT Nagpur",
    "Tell me about IIIT Butibori",
]

# Define a dictionary for Google Maps locations
LOCATION_MAPS = {
    "iiit butibori": "https://maps.app.goo.gl/D6JEFcKjNyX8TsVm7",
    "vnit nagpur": "https://maps.app.goo.gl/tp2ToBrJRDgqreuk7",
    "nit nagpur": "https://maps.app.goo.gl/tp2ToBrJRDgqreuk7",
}

# Function to find the best matching question
def get_best_match(user_input):
    match, score, _ = process.extractOne(user_input, ALLOWED_QUESTIONS, score_cutoff=65)  
    return match if score else None  

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip().lower()  

            # Check if the message is a location request
            for location in LOCATION_MAPS:
                if location in message:
                    return JsonResponse({
                        "reply": f"You can find {location.upper()} here: {LOCATION_MAPS[location]}"
                    })

            # Handle event-related queries
            if "event" in message or "schedule" in message:
                events = Event.objects.all()
                if not events:
                    return JsonResponse({"reply": "No upcoming events found."})

                event_info = "\n".join([
                    f"{event.name} - {event.date} at {event.time} in {event.location}"
                    for event in events
                ])
                return JsonResponse({"reply": f"Here are the upcoming events:\n{event_info}"})

            # Get the best-matching AI-related question
            best_match = get_best_match(message)

            if not best_match:
                return JsonResponse({"reply": "Sorry, I can only answer specific questions about AI, events, or locations."})

            # Modify prompt to limit response length
            prompt = f"""
You are an AI chatbot. Your task is to answer the following question in a clear and precise manner.

Question: {best_match}

Rules:
1. Keep the answer between 50-60 words.
2. Do not provide irrelevant information.
3. Answer in simple, easy-to-understand language.
"""

            # Call Gemini AI API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]  
            }

            response = requests.post(url, headers=headers, json=payload)
            api_response = response.json()

            if "candidates" in api_response:
                reply = api_response["candidates"][0]["content"]["parts"][0]["text"]
                return JsonResponse({"reply": reply})
            else:
                return JsonResponse({"reply": "I'm unable to answer that right now, please try another question."})

        except Exception as e:
            return JsonResponse({"reply": "An error occurred while processing your request."})

    return JsonResponse({"reply": "Invalid request method."})

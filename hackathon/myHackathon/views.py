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
    return render(request, "home.html")  # Render a simple home page

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Define the list of allowed AI-related questions
ALLOWED_QUESTIONS = [
    "hello",
    "hi",
    "What is artificial intelligence?",
    "How does machine learning work?",
    "What is the future of robotics?",
    "What is the impact of AI on jobs?",
    "What are some futuristic technologies?",
    "What is quantum computing?",
    "What are the latest trends in AI?"
]

# Function to find the best matching question
def get_best_match(user_input):
    match, score, _ = process.extractOne(user_input, ALLOWED_QUESTIONS, score_cutoff=75)  
    return match if score else None  # Return match only if score >= 75

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").strip().lower()  # Convert message to lowercase

            # Check if user is asking about events
            if "event" in message or "schedule" in message:
                events = Event.objects.all()
                if not events:
                    return JsonResponse({"reply": "No upcoming events found."})

                event_info = "\n".join([
                    f"{event.name} - {event.date} at {event.time} in {event.location}"
                    for event in events
                ])
                return JsonResponse({"reply": f"Here are the upcoming events:\n{event_info}"})

            # Get the best matching AI question
            best_match = get_best_match(message)

            if not best_match:
                return JsonResponse({"reply": "Sorry, I can only answer specific questions about AI or events."})

            # Call Gemini AI for answering allowed AI questions
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": best_match}]}]  # Use the matched question
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

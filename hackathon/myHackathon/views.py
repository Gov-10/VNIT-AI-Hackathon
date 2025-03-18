from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import requests
import os
import json  
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

def register(request):
    return render(request, 'register.html')

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event_detail.html', {'event': event})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

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
    "Tell me a tech joke",
]

# Dictionary for Google Maps locations
LOCATION_MAPS = {
    "iiit butibori": "https://maps.app.goo.gl/D6JEFcKjNyX8TsVm7",
    "vnit nagpur": "https://maps.app.goo.gl/tp2ToBrJRDgqreuk7",
}

# Predefined questions
FAQ_ANSWERS = {
    "hello": "Hello there! Welcome to the AI Tech Fest. How can I assist you today?",
    "hi": "Hi! What would you like to know about AI, events, or locations?",
    "tell me a tech joke": "Why did the AI break up with its girlfriend? She had too many issues to debug!",
    "how can i contact you": "Email: abc10@gmail.com , Phone: +91-1234567890",
}

# Function to find the best matching question
def get_best_match(user_input):
    result = process.extractOne(user_input, ALLOWED_QUESTIONS, score_cutoff=60)
    return result[0] if result else None  

def chatbot_response(request):
    if request.method == "GET":
        try:
            # Extract query parameter
            message = request.GET.get("message", "").strip().lower()

            if not message:
                return JsonResponse({"reply": "Please provide a message query."})

            # Step 1: Handle exact matches for location first
            if message in LOCATION_MAPS:
                return JsonResponse({
                    "reply": f"You can find {message.upper()} here: {LOCATION_MAPS[message]}"
                })

            # Step 2: Handle predefined FAQ answers
            if message in FAQ_ANSWERS:
                return JsonResponse({"reply": FAQ_ANSWERS[message]})

            # Step 3: Handle event queries
            if "event" in message or "schedule" in message:
                events = Event.objects.all()
                if not events:
                    return JsonResponse({"reply": "No upcoming events found."})

                event_info = "\n".join([
                    f"{event.name} - {event.date} at {event.time} in {event.location}"
                    for event in events
                ])
                return JsonResponse({"reply": f"Here are the upcoming events:\n{event_info}"})

            # Step 4: Prioritize exact matches before fuzzy matching
            best_match = message if message in ALLOWED_QUESTIONS else get_best_match(message)

            if not best_match:
                return JsonResponse({"reply": "Sorry, I can only answer specific questions about AI, events, or locations."})

            # Step 5: Ensure API Key exists before calling Gemini API
            if not GEMINI_API_KEY:
                return JsonResponse({"reply": "API key missing. Please check the server configuration."})

            # Step 6: Generate AI response using Gemini API
            prompt = f"""
            You are an AI chatbot. Your task is to answer the following question in a clear and precise manner.

            Question: {best_match}

            Rules:
            1. Keep the answer strictly between 50-60 words.
            2. Do not provide irrelevant information.
            3. Answer in simple, easy-to-understand language.
            4. Think of yourself as a subject expert.
            5. Answer in a kind and soft tone.
            6. The answer should not exceed 60 words.
            """

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}

            response = requests.post(url, headers=headers, json=payload)
            api_response = response.json()

            if "candidates" in api_response and api_response["candidates"]:
                reply = api_response["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "No valid response received.")
                return JsonResponse({"reply": reply})

            return JsonResponse({"reply": "I'm unable to fetch a response at the moment."})

        except Exception as e:
            return JsonResponse({"reply": "Sorry, I can't answer this right now."})

    return JsonResponse({"reply": "Invalid request method."})

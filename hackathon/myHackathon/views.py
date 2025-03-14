from django.shortcuts import render, get_object_or_404
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
    "Do you have any games or puzzles?",
    "Show me a cool image related to this AI Tech fest"
]

#dictionary for Google Maps locations
LOCATION_MAPS = {
    "iiit butibori": "https://maps.app.goo.gl/D6JEFcKjNyX8TsVm7",
    "vnit nagpur": "https://maps.app.goo.gl/tp2ToBrJRDgqreuk7",
}

#Predefined questions
FAQ_ANSWERS = {
    "hello": "Hello there! Welcome to the AI Tech Fest. How can I assist you today?",
    "hi": "Hi! What would you like to know about AI, events, or locations?",
    "tell me a tech joke": "Why did the AI break up with its girlfriend? She had too many issues to debug!"
}


# Function to find the best matching question
def get_best_match(user_input):
    match, score, _ = process.extractOne(user_input, ALLOWED_QUESTIONS, score_cutoff=50)  
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
            if message in FAQ_ANSWERS:
                return JsonResponse({"reply": FAQ_ANSWERS[message]})

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
1. Keep the answer strictly between 50-60 words.
2. Do not provide irrelevant information.
3. Answer in simple, easy-to-understand language.
4. Think of yourself as a subject expert.
5. Answer in a kind and soft tone
6. the answer should not exceed 60 words
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
            return JsonResponse({"reply": "Sorry, I can't answer this right now"})

    return JsonResponse({"reply": "Invalid request method."})


# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# import requests
# import os
# import json
# from django.views.decorators.csrf import csrf_exempt
# from dotenv import load_dotenv
# from rapidfuzz import process
# from .models import Event

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # AI-related allowed questions
# ALLOWED_QUESTIONS = [
#     "hello", "hi",
#     "What is artificial intelligence?",
#     "How does machine learning work?",
#     "What is the future of robotics?",
#     "What is the impact of AI on jobs?",
#     "What are some futuristic technologies?",
#     "What is quantum computing?",
#     "What are the latest trends in AI?",
#     "Tell me about NIT Nagpur",
#     "Tell me about IIIT Butibori",
#     "Tell me a tech joke",
#     "Do you have any games or puzzles?",
#     "Show me a cool image related to this AI Tech fest"
# ]

# # Predefined FAQs for direct responses
# FAQ_ANSWERS = {
#     "hello": "Hello there! Welcome to the AI Tech Fest. How can I assist you today?",
#     "hi": "Hi! What would you like to know about AI, events, or locations?",
#     "tell me a tech joke": "Why did the AI break up with its girlfriend? She had too many issues to debug!"
# }

# # Google Maps Locations
# LOCATION_MAPS = {
#     "iiit butibori": "https://maps.app.goo.gl/D6JEFcKjNyX8TsVm7",
#     "vnit nagpur": "https://maps.app.goo.gl/tp2ToBrJRDgqreuk7",
# }

# # Function to find best match from user input
# def get_best_match(user_input):
#     match, score, _ = process.extractOne(user_input, ALLOWED_QUESTIONS, score_cutoff=65)
#     return match if score else None

# @csrf_exempt
# def chatbot_response(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             message = data.get("message", "").strip().lower()

#             # 1️⃣ **Check if it's a predefined greeting**
#             if message in FAQ_ANSWERS:
#                 return JsonResponse({"reply": FAQ_ANSWERS[message]})

#             # 2️⃣ **Check for location request**
#             for location in LOCATION_MAPS:
#                 if location in message:
#                     return JsonResponse({
#                         "reply": f"You can find {location.upper()} here: {LOCATION_MAPS[location]}"
#                     })

#             # 3️⃣ **Check for specific event-related queries**
#             if "event" in message or "schedule" in message:
#                 events = Event.objects.all().order_by("date", "time")

#                 if "next" in message and events:
#                     next_event = events.first()
#                     return JsonResponse({
#                         "reply": f"The next event is {next_event.name} on {next_event.date} at {next_event.time} in {next_event.location}."
#                     })

#                 if not events:
#                     return JsonResponse({"reply": "No upcoming events found."})

#                 event_info = "\n".join([
#                     f"{event.name} - {event.date} at {event.time} in {event.location}"
#                     for event in events
#                 ])
#                 return JsonResponse({"reply": f"Here are the upcoming events:\n{event_info}"})

#             # 4️⃣ **Handle AI-related queries using fuzzy matching**
#             best_match = get_best_match(message)
#             if not best_match:
#                 return JsonResponse({"reply": "I'm not sure about that. Try asking about AI, events, or locations."})

#             # 5️⃣ **Generate AI response using Gemini API**
#             prompt = f"""
# You are an AI chatbot answering the following question clearly and concisely.

# **Question:** {best_match}

# **Rules:**
# - Answer in 50-60 words.
# - Be informative and engaging.
# - Use simple language.
# - Maintain a friendly and helpful tone.
# """

#             url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
#             headers = {"Content-Type": "application/json"}
#             payload = {"contents": [{"parts": [{"text": prompt}]}]}

#             response = requests.post(url, headers=headers, json=payload)
#             api_response = response.json()

#             if "candidates" in api_response:
#                 reply = api_response["candidates"][0]["content"]["parts"][0]["text"]
#                 return JsonResponse({"reply": reply})
#             else:
#                 return JsonResponse({"reply": "I'm unable to answer that right now. Please try another question."})

#         except Exception as e:
#             return JsonResponse({"reply": "Oops! Something went wrong. Try again later."})

#     return JsonResponse({"reply": "Invalid request method."})

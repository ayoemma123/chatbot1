
import os
import json
import joblib
import google.generativeai as genai


from google import genai
from google.genai import types
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# import the model
from .models import ChatLog  


# --- Self thousht model it is not used --- #
MODEL_PATH = os.path.join(settings.BASE_DIR, "chat", "svm_chatbot.pkl")
RESPONSES_PATH = os.path.join(settings.BASE_DIR, "chat", "responses.pkl")

model = joblib.load(MODEL_PATH)
RESPONSES = joblib.load(RESPONSES_PATH)


@csrf_exempt
def chatbot_api(request):
    try:
        # --- POST (main API use) --- #
        if request.method == "POST":
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"response": "Please enter a message."}, status=400)

            try:
                intent = model.predict([user_message])[0]
            except Exception:
                intent = None

            if not intent or intent not in RESPONSES:
                response = f"Sorry, I don't fully understand '{user_message}'. Our support staff will assist you shortly."
                ChatLog.objects.create(
                    user_message=user_message,
                    predicted_intent="unknown",
                    response_sent=response
                )
                return JsonResponse({"intent": "unknown", "response": response})

            response = RESPONSES.get(
                intent,
                f"I detected your intent as '{intent}', but I’m still learning the best answer."
            )

            ChatLog.objects.create(
                user_message=user_message,
                predicted_intent=intent,
                response_sent=response
            )

            return JsonResponse({"intent": intent, "response": response})

        # --- GET (for quick browser testing) --- #
        elif request.method == "GET":
            user_message = request.GET.get("message", "").strip()
            if not user_message:
                return JsonResponse({"message": "Chatbot API is running. Use POST or add ?message=hello"})

            try:
                intent = model.predict([user_message])[0]
            except Exception:
                intent = None

            if not intent or intent not in RESPONSES:
                response = f"Sorry, I don't fully understand '{user_message}'."
                return JsonResponse({"intent": "unknown", "response": response})

            response = RESPONSES.get(intent, f"Detected intent: {intent}")
            return JsonResponse({"intent": intent})

        # --- Other methods --- #
        else:
            return JsonResponse({"error": "Only GET and POST methods allowed"}, status=405)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# --- GEMINI API WHICH IS BEING USED --- #
FAQ_FILE_PATH = os.path.join(settings.BASE_DIR, "chat", "faq.txt")

with open(FAQ_FILE_PATH, "r", encoding="utf-8") as f:
    faq_context = f.read()


# Setup Gemini client (no configure in google-genai)
client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.0-flash-lite"

@csrf_exempt
def faq_chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")

            if not user_input:
                return JsonResponse({"error": "Message is required"}, status=400)

            # Put FAQ context + user message together
            full_prompt = f"""
            You are a chatbot that answers questions based only on these FAQs:

            {faq_context}

            User: {user_input}
            """

            contents = [
                types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)]),
            ]

            response_text = ""
            for chunk in client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(),
            ):
                if chunk.text:
                    response_text += chunk.text

            return JsonResponse({"reply": response_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
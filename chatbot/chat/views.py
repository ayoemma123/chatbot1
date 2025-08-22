from django.shortcuts import render
from django.conf import settings

import os
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# import the model
from .models import ChatLog  


# Load model & responses once (not on every request)

MODEL_PATH = os.path.join(settings.BASE_DIR, "chat", "svm_chatbot.pkl")
RESPONSES_PATH = os.path.join(settings.BASE_DIR, "chat", "responses.pkl")


model = joblib.load(MODEL_PATH)
RESPONSES = joblib.load(RESPONSES_PATH)



# API FOR THE HOMEINTERIORS 

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"response": "Please enter a message."}, status=400)

            # Predict intent
            try:
                intent = model.predict([user_message])[0]
            except Exception:
                intent = None

            # Fallback if no intent detected
            if not intent or intent not in RESPONSES:
                response = f"Sorry, I don't fully understand '{user_message}'. Our support staff will assist you shortly."
                ChatLog.objects.create(
                    user_message=user_message,
                    predicted_intent="unknown",
                    response_sent=response
                )
                return JsonResponse({"intent": "unknown", "response": response})

            # ✅ Get mapped response from RESPONSES dict
            response = RESPONSES.get(
                intent,
                f"I detected your intent as '{intent}', but I’m still learning the best answer."
            )

            # Save chat log
            ChatLog.objects.create(
                user_message=user_message,
                predicted_intent=intent,
                response_sent=response
            )

            return JsonResponse({"intent": intent})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
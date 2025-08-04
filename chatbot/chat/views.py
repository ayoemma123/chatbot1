from django.shortcuts import render

import os
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import ChatLog  # import the model

# Load model once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "svm_chatbot.pkl")
model = joblib.load(model_path)

# Simple response map
RESPONSES = {
    "greet": "Hello! How can I assist you today?",
    "ask_product": "Sure! We have phones, laptops, and shoes. What are you interested in?",
    "product_price": "Which product would you like the price for?",
    "order_status": "Please provide your order number so I can check the status.",
    "shipping_info": "Standard shipping takes 3-5 business days. Would you like express delivery?",
    "return_policy": "Our return policy allows returns within 30 days of delivery.",
    "track_order": "Please provide your tracking number to proceed.",
    "payment_methods": "We accept cards, bank transfers, and PayPal.",
    "cancel_order": "I can help with that. Please provide your order number.",
    "store_hours": "We're open Monday to Saturday from 9 AM to 9 PM.",
    "goodbye": "Thank you for visiting. Come back soon!",
    "fallback": "I'm sorry, I didn't understand that. Could you rephrase?"
}




@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Predict intent
        intent = model.predict([user_message])[0]
        response = RESPONSES.get(intent, "I'm not sure I understand. Can you rephrase?")

        # Save to database
        ChatLog.objects.create(
            user_message=user_message,
            predicted_intent=intent,
            response_sent=response
        )

        return JsonResponse({"intent": intent}) 
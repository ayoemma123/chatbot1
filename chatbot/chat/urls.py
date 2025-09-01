from django.urls import path
from . import views

urlpatterns = [   
    
    path ( "chat/", views.chatbot_api, name= "chat" ),
   # path ( "gemini/", views.gemini_api, name= "gemini" ),
    path ( "faq/", views.faq_chatbot_api, name= "faq" ),  

]

from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth.models import User

from . models import Chat

from django.utils import timezone

# for google generativeai
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
# from IPython.display import Markdown
import markdown

# For api key
import os
from dotenv import load_dotenv
load_dotenv()

# accessing api key
api_key = os.getenv('API_KEY')

# configure api key
genai.configure(api_key=api_key)

# selecting the model 
model = genai.GenerativeModel('gemini-1.5-flash')

# Markdown response
def to_markdown(text):
    text = text.replace('•', '  *')
    return markdown.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Ask gemini
def ask_gemini(message):
    response = model.generate_content(message)
    answer = to_markdown(response.text)

    return answer
    

# Create your views here.
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message)

        chat = Chat(user = request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message':message, 'response':response})
    return render(request, 'chat.html')

# login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chat')
        else:
            error_msg = 'Invaild Username or Password'
            return render(request, 'login.html', {'error_msg':error_msg})
    else:
        return render(request, 'login.html')

# logout
def logout(request):
    auth.logout(request)
    return redirect('login')

# register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chat')
            except:
                error_msg = 'Error Creating Account'
                return render(request, 'register.html', {'error_msg':error_msg})
        else:
            error_msg = 'Passwords do not match'
            return render(request, 'register.html', {'error_msg':error_msg})
        
    return render(request, 'register.html')
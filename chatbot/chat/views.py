from django.shortcuts import render
from django.http import JsonResponse

# for google generativeai
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

# For api key
import os
from dotenv import load_dotenv
load_dotenv()

# accessing api key
api_key = os.getenv('API_KEY')

# selecting the model 
model = genai.GenerativeModel('gemini-1.5-flash')

# Markdown response
def to_markdown(text):
    text = text.replace('.', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

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
        return JsonResponse({'message':message, 'response':response})
    return render(request, 'chat.html')
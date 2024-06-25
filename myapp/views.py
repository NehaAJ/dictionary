from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # Note: Renamed to avoid conflict with view name
from django.urls import reverse
from django.http import JsonResponse
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Authentication successful, redirect to the about page
            return redirect(reverse('dictionary_search'))
        else:
            # Authentication failed, add an error message to the context
            context = {'error': 'Invalid username or password'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')

import requests
from django.shortcuts import render

def dictionary_search(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            return render(request, 'dictionary_search.html', {'data': data, 'word': word})
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as err:
            error_message = f"Error occurred: {err}"
        except ValueError:
            error_message = "Invalid response received from dictionary API"
        return render(request, 'dictionary_search.html', {'error': error_message, 'word': word})

    return render(request, 'dictionary_search.html')
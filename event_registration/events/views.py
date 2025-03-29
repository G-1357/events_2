from django.shortcuts import render, redirect
from .forms import LoginForm, EventForm
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.contrib.auth import authenticate, login

def start(request):
    return render(request, 'start.html')

def enter(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'enter.html', {'form': form})


def forma(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EventForm()
    return render(request, 'forma.html', {'form': form})

def profile(request):
    organizer_name = request.user.username if request.user.is_authenticated else 'Гость'
    organizer_email = request.user.email if request.user.is_authenticated else 'example@example.com'

    context = {
        'organizer_name': organizer_name,
        'organizer_email': organizer_email,
    }
    return render(request, 'profile.html', context)

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
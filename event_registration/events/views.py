from django.shortcuts import render, redirect
from .forms import LoginForm, EventForm
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

def start(request):
    return render(request, 'start.html')

def enter(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('forma')
    else:
        form = LoginForm()
    return render(request, 'enter.html', {'form': form})

def forma(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('start')  # Переход обратно на стартовую страницу
    else:
        form = EventForm()
    return render(request, 'forma.html', {'form': form})

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
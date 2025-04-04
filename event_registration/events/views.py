from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, EventForm
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

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
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('profile')
    else:
        form = EventForm()
    return render(request, 'forma.html', {'form': form})

def profile(request):
    organizer_name = request.user.username if request.user.is_authenticated else 'Гость'
    organizer_email = request.user.email if request.user.is_authenticated else 'example@example.com'

    events = Event.objects.filter(organizer=request.user)

    context = {
        'organizer_name': organizer_name,
        'organizer_email': organizer_email,
        'events': events,
    }
    return render(request, 'profile.html', context)


def event_creation_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if title and date and description:
            event = Event(
                title=title,
                date=date,
                description=description,
                image=image,
                organizer=request.user
            )
            event.organizer_id=1
            event.save()
            return redirect('profile')
        else:
            return render(request, 'event_form.html', {'error': 'Заполните все обязательные поля.'})
    else:
        return render(request, 'event_form.html')
def organizer_profile_view(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'organizer_profile.html', {
        'organizer_name': request.user.username,
        'organizer_email': request.user.email,
        'events': events
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def register_attendee(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":

        event.attendee_count += 1
        event.save()
        messages.success(request, f'К вашему мероприятию "{event.title}" зарегистрировался новый участник.')

        return redirect('event_detail', event_id=event.id)

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие успешно обновлено!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        messages.success(request, 'Мероприятие успешно удалено!')
        return redirect('profile')

    return render(request, 'delete_event.html', {'event': event})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие успешно обновлено!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        messages.success(request, 'Мероприятие успешно удалено!')
        return redirect('profile')

    return render(request, 'delete_event.html', {'event': event})


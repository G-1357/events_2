from django.urls import path
from .views import start, enter, forma, EventListCreateAPIView, EventDetailAPIView

urlpatterns = [
    path('', start, name='start'),
    path('enter/', enter, name='enter'),
    path('forma/', forma, name='forma'),
    path('api/events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('api/events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
]
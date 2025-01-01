from django.urls import path
from .api_views import EventAPI, AttendeeAPI, TaskAPI, AssignmentAPI
from .views import register_user, login_user

urlpatterns = [
    path('events/', EventAPI.as_view(), name='event_list'),
    path('events/<int:pk>/', EventAPI.as_view(), name='event_detail'),
    path('attendees/', AttendeeAPI.as_view(), name='attendee_list'),
    path('attendees/<int:pk>/', AttendeeAPI.as_view(), name='attendee_detail'),
    path('tasks/', TaskAPI.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskAPI.as_view(), name='task_detail'),
    path('assignments/', AssignmentAPI.as_view(), name='assignment_list'),  
    path('assignments/<int:pk>/',AssignmentAPI.as_view(), name='assignment_detail'),  
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
]

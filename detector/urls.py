from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('api/analyze/', views.api_analyze, name='api_analyze'),
]

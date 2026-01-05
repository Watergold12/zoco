from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('story/', views.story, name='story'),
]
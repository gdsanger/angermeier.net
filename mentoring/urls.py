from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bewerben/', views.apply, name='apply'),
    path('bewerben/danke/', views.apply_success, name='apply_success'),
]

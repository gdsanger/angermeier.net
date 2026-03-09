from django.urls import path
from . import views
from . import views as mentoring_views

urlpatterns = [
    path('', views.index, name='index'),
    path('bewerben/', views.apply, name='apply'),
    path('bewerben/danke/', views.apply_success, name='apply_success'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path("robots.txt", mentoring_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", mentoring_views.sitemap_xml, name="sitemap_xml"),
]

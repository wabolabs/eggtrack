from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_log, name='daily_log'),
    path('hens/', views.hen_list, name='hen_list'),
    path('hens/add/', views.hen_add, name='hen_add'),
    path('hens/<int:hen_id>/photo/', views.hen_update_photo, name='hen_update_photo'),
    path('stats/', views.stats, name='stats'),
    path('history/', views.edit_history, name='edit_history'),
    path('breeds/', views.breed_list, name='breed_list'),
    path('breeds/add/', views.breed_add, name='breed_add'),
    path('colors/', views.color_list, name='color_list'),
    path('colors/add/', views.color_add, name='color_add'),
]

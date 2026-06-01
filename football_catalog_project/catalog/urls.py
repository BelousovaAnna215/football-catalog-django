from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('player/<int:id>/', views.player_detail, name='player_detail'),
    path('add/', views.add_player, name='add_player'),
]

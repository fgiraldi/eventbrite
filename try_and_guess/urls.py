from django.urls import path
from . import views
# development mode, static files
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
   path('', views.welcome, name='index'),
   path('user_starts/', views.user_starts, name='user_starts'),
   path('machine_starts/', views.machine_starts, name='machine_starts'),
   path('games/<int:game_id>/user_guesses/',
        views.user_guesses,
        name='user_guesses'),
   path('games/<int:game_id>/machine_guesses/',
        views.machine_guesses,
        name='machine_guesses'),
   path('games/<int:game_id>/cancel_game/',
        views.cancel_game,
        name='cancel_game')

]

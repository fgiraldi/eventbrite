from django.urls import path
from . import views
# development mode, static files
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
   path('', views.welcome, name='index'),
   path('user_starts/', views.user_starts, name='user_starts'),
   path('machine_starts/', views.machine_starts, name='machine_starts'),
]

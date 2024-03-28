# testing_log/urls.py
from django.urls import path
from testing_log import views
# from .views import hello_world

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]

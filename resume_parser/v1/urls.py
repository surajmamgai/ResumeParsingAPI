from django.urls import path
from v1 import views

urlpatterns = [
    path("", views.home, name="home"),
    path("extract/", views.extract, name="extract"),
]
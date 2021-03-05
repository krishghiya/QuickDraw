from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data/", views.predict, name="predict"),
]
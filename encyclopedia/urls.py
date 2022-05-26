from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:topic>", views.topic, name="topic"),
    path("<str:topic>/edit", views.edit, name="edit"),
    path("error/", views.error, name="error"),
    path("matches/", views.matches, name="matches"),
    path("random/", views.random, name="random"),
    path("new/", views.new, name="new"),
    path("save/", views.save, name="save")
]

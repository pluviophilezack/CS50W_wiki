from django.urls import path

from . import views

# app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/random", views.random, name="random"),
    path("wiki/new_page", views.new_page, name="new_page"),
    path("wiki/edit_page/<str:original_title>", views.edit_page, name="edit_page"),
    path("wiki/<str:title>", views.entry, name="entry")
]

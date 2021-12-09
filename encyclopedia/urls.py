from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("apologize", views.apologize, name="apologize"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
    path("edit_<str:title>", views.edit_page, name="edit_page"),
    path("wiki/<str:title>", views.entries, name="entries"),
]

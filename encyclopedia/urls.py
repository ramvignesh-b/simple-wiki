from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view, name="view"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path('random', views.random_page, name="random"),
    path('create', views.create, name="create")
]

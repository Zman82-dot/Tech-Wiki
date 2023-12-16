from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newWiki", views.newWiki, name="newWiki"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path("search", views.search, name="search")
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>", views.blogs_by_category, name="blogsByCategory"),
    path("blog/<slug:slug>", views.getBlog, name="getBlog"),
    path("content/<slug:slug>", views.getContent, name="getContent"),
    # path("contactus", views.getContent, name="getContent")
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.SiteView.home, name="home"),
    path("category/<slug:slug>", views.SiteView.blogs_by_category, name="blogsByCategory"),
    path("tag/<slug:slug>", views.SiteView.blogs_by_tag, name="blogsByTag"),
    path("blog/<slug:slug>", views.SiteView.getBlog, name="getBlog"),
    path("content/<slug:slug>", views.SiteView.getContent, name="getContent"),
    # path("contactus", views.getContent, name="getContent")
]

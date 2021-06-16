from django.urls import path
from . import views
from django.contrib import admin

admin.site.site_header = "Admin Panel"
admin.site.site_title = "My Site Title"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>", views.blogs_by_category, name="blogsByCategory"),
    path("blog/<slug:slug>", views.getBlog, name="getBlog")
]

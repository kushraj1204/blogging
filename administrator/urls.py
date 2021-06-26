from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='adminHome'),
    path('login', views.Login.as_view(), name='adminLogin'),
    path('logout', views.Logout.as_view(), name='adminLogout'),

    path('users', views.UserView.get_list, name='adminUserList'),
    path('users/add', views.UserView.add, name='adminUserAdd'),
    path('user/<int:pk>/edit', views.UserView.as_view(), name='adminUserDetail'),
    path('user/<int:pk>/delete', views.UserView.delete, name='adminUserDelete'),

    path('groups', views.GroupView.get_list, name='adminGroupList'),
    path('groups/add', views.GroupView.add, name='adminGroupAdd'),
    path('group/<int:pk>/edit', views.GroupView.as_view(), name='adminGroupDetail'),
    path('group/<int:pk>/delete', views.GroupView.delete, name='adminGroupDelete'),

    path('contents', views.ContentView.get_list, name='adminContentList'),
    path('contents/add', views.ContentView.add, name='adminContentAdd'),
    path('content/<int:pk>/edit', views.ContentView.as_view(), name='adminContentDetail'),
    path('content/<int:pk>/delete', views.ContentView.delete, name='adminContentDelete'),

    path('categories', views.CategoryView.get_list, name='adminCategoryList'),
    path('categories/add', views.CategoryView.add, name='adminCategoryAdd'),
    path('category/<int:pk>/edit', views.CategoryView.as_view(), name='adminCategoryDetail'),
    path('category/<int:pk>/delete', views.CategoryView.delete, name='adminCategoryDelete'),

    path('blogs', views.BlogView.get_list, name='adminBlogList'),
    path('blogs/add', views.BlogView.add, name='adminBlogAdd'),
    path('blog/<int:pk>/edit', views.BlogView.as_view(), name='adminBlogDetail'),
    path('blog/<int:pk>/delete', views.BlogView.delete, name='adminBlogDelete'),

    path('imageupload', views.Images.as_view(), name='imageUpload'),
    path('commonmedia/imageList', views.Images.getImageList, name='imageList'),
    path('settings', views.SettingsView.as_view(), name='adminSettings'),

]

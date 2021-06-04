from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='adminHome'),
    path('login', views.Login.as_view(), name='adminLogin'),
    path('logout', views.Logout.as_view(), name='adminLogout'),
    path('users', views.Users.as_view(), name='adminUsers'),
    path('user/<int:pk>', views.User.as_view(), name='adminUserDetail'),
    path('user/add_new', views.User.add_user, name='adminAddUser'),
    path('user/imageupload', views.Images.as_view(), name='userImageUpload'),
]

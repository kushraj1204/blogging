from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='adminHome'),
    path('login', views.Login.as_view(), name='adminLogin'),
    path('logout', views.Logout.as_view(), name='adminLogout'),
    path('users', views.Users.as_view(), name='adminUsers'),
    path('user/<int:pk>', views.User.as_view(), name='adminUserDetail'),
    path('user/add_new', views.User.add_user, name='adminAddUser'),
    path('user/delete', views.User.delete_user, name='adminDeleteUser'),
    path('groups', views.GroupsView.as_view(), name='adminGroups'),
    path('group/<int:pk>', views.GroupView.as_view(), name='adminGroupDetail'),
    path('group/add_new', views.GroupView.add_group, name='adminAddGroup'),
    path('group/delete', views.GroupView.delete_group, name='adminDeleteGroup'),
    path('user/imageupload', views.Images.as_view(), name='userImageUpload'),
]

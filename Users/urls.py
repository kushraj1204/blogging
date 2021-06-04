from django.urls import path
from .views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView, SignUpView, ProfileView, ActivateView, \
    ProfileUpdate

app_name = "accounts"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView, name='signup'),
    path('activate/<uidb64>/<token>/', ActivateView, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView, name='detail'),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/update/', ProfileUpdate, name='profile_update'),

]

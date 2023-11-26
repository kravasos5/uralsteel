from django.urls import path

from visual.views import *

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('ladles/', Ladles.as_view(), name='ladles'),
    path('cranes/', Cranes.as_view(), name='cranes'),
    path('access-denied/', AccessDenied.as_view(), name='access-denied'),
    path('form/', Form.as_view(), name='form'),
    # маршрут профиля
    path('profile/<slug:slug>/', EmployeeProfile.as_view(), name='profile'),
    # маршруты входа/выхода
    path('profile/login/', LoginView.as_view(), name='login'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    # маршруты сброса пароля
    path('profile/password/reset/starting/', PasswordResetStarting.as_view(), name='pass-reset-starting'),
    path('profile/password/reset/confirm/', PasswordResetConfrim.as_view(), name='pass-reset-confirm'),
    path('profile/password/reset/complete/', PasswordResetComplete.as_view(), name='pass-reset-complete'),
    path('profile/password/reset/', PasswordReset.as_view(), name='password-reset'),

]
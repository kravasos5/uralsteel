from django.urls import path

from visual.views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('ladles/', LadlesView.as_view(), name='ladles'),
    path('cranes/', CranesView.as_view(), name='cranes'),
    path('accident/', AccidentView.as_view(), name='accident'),
    # маршруты входа/выхода
    path('login/', EmployeeLoginView.as_view(), name='login'),
    path('logout/', EmployeeLogoutView.as_view(), name='logout'),
    # запрет доступа
    path('access-denied/', AccessDeniedView.as_view(), name='access-denied'),
    # маршруты сброса пароля
    path('profile/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirm.as_view(), name='pass-reset-confirm'),
    path('profile/password/reset/starting/', PasswordResetStarting.as_view(), name='pass-reset-starting'),
    path('profile/password/reset/complete/', PasswordResetComplete.as_view(), name='pass-reset-complete'),
    path('profile/password/reset/', PasswordReset.as_view(), name='password-reset'),
    # маршрут профиля
    path('profile/<slug:slug>/change/', ChangeEmployeeInfoView.as_view(), name='profile-change'),
    path('profile/<slug:slug>/', EmployeeProfile.as_view(), name='profile'),
]
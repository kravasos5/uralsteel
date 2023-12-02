from django.urls import path

from visual.views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    # ковши
    path('ladles/', LadlesView.as_view(), name='ladles'),
    # краны
    path('cranes/', CranesView.as_view(), name='cranes'),
    # проишествия
    # маршруты начала дополнения
    path('accident/ladle/detail/starting/<int:pk>/', LadleAccidentDetailStartingView.as_view(), name='accident-ladle-detail-starting'),
    path('accident/crane/detail/starting/<int:pk>/', CraneAccidentDetailStartingView.as_view(), name='accident-crane-detail-starting'),
    path('accident/aggregate/detail/starting/<int:pk>/', AggregateAccidentDetailStartingView.as_view(), name='accident-aggregate-detail-starting'),
    # маршруты дополнения отчёта
    path('accident/ladle/detail/<int:pk>/', LadleAccidentDetailView.as_view(), name='accident-ladle-detail'),
    path('accident/crane/detail/<int:pk>/', CraneAccidentDetailView.as_view(), name='accident-crane-detail'),
    path('accident/aggregate/detail/<int:pk>/', AggregateAccidentDetailView.as_view(), name='accident-aggregate-detail'),
    # маршруты составления отчёта о проишествии
    path('accident/ladle/', LadleAccidentView.as_view(), name='accident-ladle'),
    path('accident/crane/', CraneAccidentView.as_view(), name='accident-crane'),
    path('accident/aggregate/', AggregateAccidentView.as_view(), name='accident-aggregate'),
    # маршрут начала составления отчёта о проишествии
    path('accident/starting/', AccidentStartingView.as_view(), name='accident-starting'),
    # система разграничения доступа
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
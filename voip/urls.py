from django.urls import path

from . import views

urlpatterns = [
    path('voip/', views.VoipView.as_view(), name='voip'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
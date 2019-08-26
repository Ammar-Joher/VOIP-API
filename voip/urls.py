from django.urls import path

from . import views

urlpatterns = [
    path('voip/', views.voipView.as_view(), name='voip'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView, name='logout'),
]
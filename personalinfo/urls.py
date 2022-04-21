from django.urls import path
from . import views

urlpatterns = [
    path('', views.toLogin, name="to_Login"),
    path('toregister/', views.toRegister, name="to_Register"),
    path('register/', views.Register, name="Register"),
    path('logout/', views.logout, name="logout"),
    path('monitor/', views.monitor, name="monitor"),
]
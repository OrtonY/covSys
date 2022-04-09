from django.urls import path
from . import views

urlpatterns = [
    path('', views.toLogin, name="to_Login"),
    path('a_login/', views.toAlogin, name="a_Login"),
    path('u_a_login/', views.toUlogin, name="u_Login"),
    path('a_navigation/', views.Login, name="a_nav"),
    path('u_navigation/', views.Login, name="u_nav"),
    path('toregister/', views.toRegister, name="to_Register"),
    path('register/', views.Register, name="Register"),
    path('logout/', views.logout, name="logout"),
    path('u_info/<str:u_id>', views.u_info, name="u_info")
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.toLogin),
    path('navigation/', views.Login),
    path('toregister/', views.toRegister),
    path('register/', views.Register),
]
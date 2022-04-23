from django.urls import path
from . import views

urlpatterns = [
    path('u_login/', views.toUlogin, name="u_Login"),
    path('u_navigation/', views.u_Login, name="u_nav"),
    path('u_navigation/<str:u_id>', views.u_return, name="u_return"),
    path('u_info/<str:u_id>', views.u_info, name="u_info"),
    path('u_schedul/<str:u_id>', views.to_u_schedul, name='u_schedul'),
    path('schedul/<str:u_id>', views.u_schedul, name='schedul'),
    path('u_go_out/<str:u_id>', views.to_u_go_out, name="u_go_out"),
    path('go_out/<str:u_id>', views.u_go_out, name="go_out"),
    path('u_covid_test/<str:u_id>', views.to_u_covid_test, name="u_covid_test"),
    path('covid_test/<str:u_id>', views.u_covid_test, name="covid_test"),
    path('u_daycard/<str:u_id>', views.to_u_daycard, name="u_daycard"),
    path('daycard/<str:u_id>', views.u_daycard, name="daycard"),
    path('u_inout_door/<str:u_id>', views.to_u_inout_door, name="u_inout_door"),
    path('inout_door/<str:u_id>', views.u_inout_door, name="inout_door"),
    path('u_interfacciami/<str:u_id>', views.u_interfacciami, name="u_interfacciami"),
    path('u_my_schedule/<str:u_id>', views.u_my_schedule, name="u_my_schedule"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.toLogin, name="to_Login"),
    path('a_login/', views.toAlogin, name="a_Login"),
    path('u_login/', views.toUlogin, name="u_Login"),
    path('a_navigation/', views.a_Login, name="a_nav"),
    path('u_navigation/', views.u_Login, name="u_nav"),
    path('toregister/', views.toRegister, name="to_Register"),
    path('register/', views.Register, name="Register"),
    path('logout/', views.logout, name="logout"),
    path('tobatch/', views.to_batch, name="batch"),
    path('batch_upload/', views.excel_upload, name="batch_upload"),
    path('u_navigation/<str:u_id>', views.u_return, name="u_return"),
    path('a_navigation/admin/', views.a_return, name="a_return"),
    path('u_info/<str:u_id>', views.u_info, name="u_info"),
    path('a_u_info/', views.a_u_info, name="a_u_info"),
    path('a_bed_check/', views.a_bed_check, name="a_bed_check"),
    path('a_day_clock/', views.a_day_clock, name="a_day_clock"),
    path('a_health_query/', views.a_health_query, name="a_health_query"),
    path('a_inout_query/', views.a_inout_query, name="a_inout_query"),
    path('a_examine/', views.a_examine, name="a_examine"),
]
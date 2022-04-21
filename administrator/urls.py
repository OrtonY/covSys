from django.urls import path
from . import views

urlpatterns = [
    path('a_login/', views.toAlogin, name="a_Login"),
    path('a_navigation/', views.a_Login, name="a_nav"),
    path('tobatch/', views.to_batch, name="batch"),
    path('batch_upload/', views.excel_upload, name="batch_upload"),
    path('a_navigation/admin/', views.a_return, name="a_return"),
    path('a_u_info/', views.a_u_info, name="a_u_info"),
    path('a_day_clock/<str:u_id>', views.a_day_clock, name="a_day_clock"),
    path('a_inout_query/', views.a_inout_query, name="a_inout_query"),
    path('a_examine/', views.a_examine, name="a_examine"),
    path('to_a_f_examine/<str:l_id>', views.to_a_f_examine, name="to_a_f_examine"),
    path('a_f_examine/<str:l_id>', views.a_f_examine, name="a_f_examine"),
    path('a_dayclock_info/', views.a_dayclock_info, name="a_dayclock_info"),
    path('a_quarantine_info/', views.a_quarantine_info, name="a_quarantine_info"),
    path('a_t_quarantine/', views.a_t_quarantine, name="a_t_quarantine"),
    path('to_a_quarantine_up/<str:u_id>', views.to_a_quarantine_up, name="to_a_quarantine_up"),
    path('a_quarantine_up/<str:u_id>', views.a_quarantine_up, name="a_quarantine_up"),
    path('a_quarantine_list_up/', views.to_a_quarantine_list_up, name="a_quarantine_list_up"),
    path('to_a_passphrase_up/', views.to_a_passphrase_up, name="to_a_passphrase_up"),
    path('a_passphrase_up/<str:l_id>', views.a_passphrase_up, name="a_passphrase_up"),
    path('to_a_healthcode_up/', views.to_a_healthcode_up, name="to_a_healthcode_up"),
    path('a_healthcode_up/<str:l_id>', views.a_healthcode_up, name="a_healthcode_up"),
    path('to_a_covlocation_up/', views.to_a_covlocation_up, name="to_a_covlocation_up"),
    path('a_covlocation_up/<str:l_id>', views.a_covlocation_up, name="a_covlocation_up"),
]
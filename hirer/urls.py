from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.show_profile),
    path('profile', views.show_profile),
    path('edit_profile/<str:id>', views.edit_profile),
    path('update_profile/<str:id>',views.update_profile),
    path('freelancelist', views.freelancelist),
    path('postjob', views.postjob),
    path('paystatus', views.paystatus),
    path('workstatus', views.workstatus),
    path('login', views.login),
    path('logout', views.logout),
    path('signup', views.user_signup),
    path('project_bid_rate', views.project_biding_rate),
    path('bid_rate_show/<str:id>/<str:end_date>', views.bid_rate_show),
    path('project_bidding_approval/<int:id>/<str:end_date>', views.project_bidding_approval),
    path('payment_given/<str:id>', views.payment_given),
    path('delete_project/<str:id>',views.delete_project),
    path('handlerequest/', views.handlerequest),
    


]
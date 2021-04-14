from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('jobfeed', views.jobfeed),
    path('signup', views.user_signup),
    path('logout', views.logout),
    path('login', views.login),
    path('report', views.report),
    path('profile', views.show_profile),
    path('edit_profile/<str:id>', views.edit_profile),
    path('update_profile/<str:id>',views.update_profile),
    path('contact', views.contact),
    path('bidding_rate/<str:id>', views.bidding_rate),
    path('bidding_starting_progress/<int:id>', views.bidding_starting_progress),
    path('bidding_intermediate_progress/<int:id>', views.bidding_intermediate_progress),
    path('bidding_mediate_progress/<int:id>', views.bidding_mediate_progress),
    path('bidding_finished_progress/<int:id>', views.bidding_finished_progress),
    path('bidding_completed_progress/<int:id>', views.bidding_completed_progress),
    path('registration', views.registration),
    
    
    
]
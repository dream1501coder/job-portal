from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index,name='index'),
    path('jobfeed', views.jobfeed,name="jobfeed"),
    path('signup', views.user_signup,name="signup"),
    path('logout', views.logout,name="logout"),
    path('login', views.login,name="login"),
    path('report', views.report,name="report"),
    path('profile', views.show_profile,name="profile"),
    path('edit_profile/<str:id>', views.edit_profile,name="edit_profile"),
    path('update_profile/<str:id>',views.update_profile,name="update_profile"),
    path('contact', views.contact,name="contact"),
    path('bidding_rate/<str:id>', views.bidding_rate,name="bidding_rate"),
    path('bidding_starting_progress/<int:id>', views.bidding_starting_progress,name="bidding_starting_progress"),
    path('bidding_intermediate_progress/<int:id>', views.bidding_intermediate_progress,name="bidding_intermediate_progress"),
    path('bidding_mediate_progress/<int:id>', views.bidding_mediate_progress,name="bidding_mediate_progress"),
    path('bidding_finished_progress/<int:id>', views.bidding_finished_progress,name="bidding_finished_progress"),
    path('bidding_completed_progress/<int:id>', views.bidding_completed_progress,name="bidding_completed_progress"),
    path('registration', views.registration,name="registration"),
    path('search', views.search,name="search"),
    
    
    
]
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('', views.index,name='index'),
    path('jobfeed', views.jobfeed,name="jobfeed"),
    path('signup', views.user_signup,name="signup"),
    path('logout', views.logout,name="logout"),
    path('login', views.login,name="login"),
    path('logins', views.logins,name="logins"),
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


    # url('^', include('django.contrib.auth.urls')),      
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='freelancer/password/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='freelancer/password/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='freelancer/password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='freelancer/password/password_reset_complete.html'),name='password_reset_complete'),

    # path('accounts/', include('django.contrib.auth.urls')),
]

   
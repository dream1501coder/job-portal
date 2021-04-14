from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.show_profile),
    path('profile', views.show_profile),
    path('freelancer', views.freelancer),
    path('hirer', views.hirer),
    path('paymentsection', views.paymentsection),
    path('projectbids', views.projectbids),
    path('reports', views.reports),
    path('login', views.login),
    path('logout', views.logout),
    path('Project', views.project_status),
    path('hirer_delete/<int:id>', views.hirer_delete),
	path('hirer_activation/<int:id>', views.hirer_activation),
	path('freelance_data_delete/<int:id>', views.freelance_data_delete),
    path('project_approve/<int:id>', views.project_approve),
    path('bid_rate_show', views.bid_rate_show),
    path('freelance_data_active/<int:id>', views.freelance_data_active),
    path('freelance_data_delete/<int:id>', views.freelance_data_delete)
       
]
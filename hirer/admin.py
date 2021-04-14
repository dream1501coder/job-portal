from django.contrib import admin
from .models import comment, project_bid_rate, payment_report


admin.site.register(comment)
admin.site.register(project_bid_rate)
admin.site.register(payment_report)

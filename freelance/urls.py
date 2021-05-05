from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('freelancer.urls')),
    path('admin/', admin.site.urls),
    path('admin1/', include('admin1.urls')),
    path('hirer/', include('hirer.urls')),
    path('freelancer/', include('freelancer.urls')),

    
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
    
# ]

   
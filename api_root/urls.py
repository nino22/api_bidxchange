from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_bidxchange.urls'), name='api_bidxchange'),
    path('sites/', include('api_bidxchange.urls2'), name='api_bidxchangeSites')
]

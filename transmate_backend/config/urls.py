from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/vehicles/', include('apps.vehicles.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/trips/', include('apps.trips.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/ratings/', include('apps.ratings.urls')),
    path('api/complaints/', include('apps.complaints.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('api/maintenance/', include('apps.maintenance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

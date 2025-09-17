from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path('user/',include("accounts.urls")),
    path('parcels/',include("parcels.urls")),
    path('logistics/',include("logistics.urls")),
    path('billing/',include("billing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
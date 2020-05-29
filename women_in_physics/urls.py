from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r"admin/", admin.site.urls),
    url(r"", include("django.contrib.auth.urls")),
    url(r"", include("women_in_physics.apps.home.urls")),
    url(r"", include("women_in_physics.apps.classroom.urls")),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


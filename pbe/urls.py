from django.apps import apps
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),

    path('', include(apps.get_app_config('oscar').urls[0])),

    path("api/", include("oscarapi.urls")),
]
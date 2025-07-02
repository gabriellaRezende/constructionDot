from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from profiles.views import LoginRegisterClientView
from django.conf.urls.static import static
from django.conf import settings
from pbe.views import CustomAddToBasketView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),

    path('basket/add/', CustomAddToBasketView.as_view(), name='basket:add'),

    path('accounts/login/', LoginRegisterClientView.as_view(), name='login'),  # Isto precisa estar antes do include do Oscar

    path('', include(apps.get_app_config('oscar').urls[0])),

    path("api/", include("oscarapi.urls")),

    path('accounts/', include('profiles.urls')),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    path('', include('profiles.urls')),

    path('api/', include('api.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
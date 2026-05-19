from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import admin as custom_admin  # ← ADD THIS LINE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('leagues/', include('leagues.urls')),
    path('players/', include('players.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
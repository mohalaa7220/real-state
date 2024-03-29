
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/product/', include('products.urls')),
    path('api/order/', include('order.urls')),
    path('api/', include('comments.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('matrimony.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'செம்போடையார் வன்னியர் திருமண மையம்'
admin.site.site_title = 'செம்போடையார்'
admin.site.index_title = 'நிர்வாக பலகை'

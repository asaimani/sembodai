from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('matrimony.urls')),
    # Serve media files in production
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

admin.site.site_header = 'செம்போடையார் வன்னியர் திருமண மையம்'
admin.site.site_title = 'செம்போடையார்'
admin.site.index_title = 'நிர்வாக பலகை'
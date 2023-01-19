from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),#It gets every routes in core views file routes
    path('api/',include('base.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#It will include in "urlpatterns" files updloaded by users. It means that the images will have a own URL
#
#
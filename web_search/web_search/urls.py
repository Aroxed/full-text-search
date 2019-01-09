from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('indexing/', include('apps.indexing.urls')),
    path('', include('apps.searching.urls'))
]

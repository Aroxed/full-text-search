from django.urls import path
from .views import FileIndexView, file_index_clean

app_name = 'indexing'

urlpatterns = [

    path('file-index', FileIndexView.as_view(), name='file_index'),
    path('file-index-clean', file_index_clean, name='file_index_clean'),
]
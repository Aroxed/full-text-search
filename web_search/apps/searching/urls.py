from django.urls import path
from apps.searching.views import HomeView, SearchHomeView, DocDetailView

app_name = 'searching'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchHomeView.as_view(), name='search_home'),
    path('detail_doc/<str:url>/<str:query>', DocDetailView.as_view(), name='detail_doc'),

]
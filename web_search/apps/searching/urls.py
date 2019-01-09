from django.urls import path
from apps.searching.views import HomeView, SearchHomeView

app_name = 'searching'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchHomeView.as_view(), name='search_home'),
]
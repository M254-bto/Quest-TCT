from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChildViewSet


urlpatterns = [
path('', ChildViewSet.as_view({'get': 'list',
                                        'post': 'create'}), name='children-list')
]
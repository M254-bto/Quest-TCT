from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChildViewSet, SearchChildView, CheckInView, CheckOutView, ChildrenNotCheckedOut, AttendanceCount, MonthlyAttendance



urlpatterns = [
path('', ChildViewSet.as_view({'get': 'list',
                                        'post': 'create'}), name='children-list'),
path('<int:pk>/', ChildViewSet.as_view({'get': 'retrieve'}), name='child-detail'),
path('search/', SearchChildView.as_view(), name='search-child'),
path('check-in/', CheckInView.as_view(), name='check-in'),
path('check-out/', CheckOutView.as_view(), name='check-out'),
path('unchecked/', ChildrenNotCheckedOut.as_view(), name='not-checked-out'),
path('count/', AttendanceCount.as_view(), name='children-count'),
path('monthly-attendance/', MonthlyAttendance.as_view(), name='monthly-attendance'),
]



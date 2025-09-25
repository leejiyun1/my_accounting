# apps/schedules/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryListCreateView, CategoryDetailView, ScheduleViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
] + router.urls
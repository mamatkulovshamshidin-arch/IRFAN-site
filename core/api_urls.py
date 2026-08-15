from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, FAQViewSet, LessonViewSet, NewsViewSet, TeacherViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-category')
router.register('teachers', TeacherViewSet, basename='api-teacher')
router.register('lessons', LessonViewSet, basename='api-lesson')
router.register('news', NewsViewSet, basename='api-news')
router.register('faq', FAQViewSet, basename='api-faq')

urlpatterns = [path('', include(router.urls))]

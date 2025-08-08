
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    Login, 
    BKTViewSet, 
    QuizViewSet, 
    TeacherViewSet
)


# DRF Router for all API endpoints creates quick url routing without
# explicit definition.

# Login has a basename due to it being a non-model view.

router = DefaultRouter()
router.register(r'login', Login, basename='login')
router.register(r'teacher', TeacherViewSet)
router.register(r'bktvalues', BKTViewSet)
router.register(r'quiz', QuizViewSet)


# Patterns for admin portal and standard are included in the patterns array.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

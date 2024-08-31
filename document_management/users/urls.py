from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'login', LoginView, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]

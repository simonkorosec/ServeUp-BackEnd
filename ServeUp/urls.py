from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ServeUp.Views import views

# Create a router and register ViewSets with it
router = DefaultRouter()
router.register(r'restaurant', views.RestavracijaViewSet, basename="restaurant")
router.register(r'admin_user', views.AdminUporabnikViewSet, basename="admin_user")
router.register(r'user', views.UporabnikViewSet, basename="user")
router.register(r'restaurant_type', views.TipRestavracijeViewSet, basename="restaurant_type")
router.register(r'orders', views.NarociloViewSet, basename="order")
router.register(r'meals', views.JedViewSet, basename="meal")

# The API URLs are determined by the router
urlpatterns = [
    path('api/', include(router.urls)),
]

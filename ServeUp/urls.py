from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ServeUp import views

# Create a router and register ViewSets with it
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)

# The API URLs are determined by the router
urlpatterns = [
    path('api/', include(router.urls))
]

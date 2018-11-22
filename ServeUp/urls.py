from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ServeUp.Views import views

# Create a router and register ViewSets with it
router = DefaultRouter()
router.register(r'restavracija', views.RestavracijaViewSet)
router.register(r'posta', views.PostaViewSet, basename="posta")
router.register(r'uporabnik', views.UporabnikViewSet, basename="uporabnik")

# The API URLs are determined by the router
urlpatterns = [
    path('api/', include(router.urls)),

]

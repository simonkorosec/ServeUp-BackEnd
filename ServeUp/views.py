from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from ServeUp.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

from rest_framework import generics, permissions

# Create your views here.
from api.serializers import UserSerializer, StorySerializer
from blogengine.models import User, Story

class UserList(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
        ]

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    looku_field = 'username'
    
class StoryList(generics.ListCreateAPIView):
    model = Story
    serializer_class = StorySerializer
    permission_classes = [
        permissions.AllowAny
        ]
        
class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Story
    serializer_class = StorySerializer
    permission_classes = [
        permissions.AllowAny
        ]

class UserStoryList(generics.ListAPIView):
    model = Story
    serializer_class = StorySerializer
    
    def get_queryset(self):
        queryset = super(UserStoryList, self).get_queryset()
        return queryset.filter(auther__username=self.kwargs.get('username'))s

from rest_framework import serializers

from blogengine.models import Story, User

class UserSerializer(serializers.ModelSerializer):
    #stories = serializers.HyperlinkedIdentityField('stories', view_name='userstory-list', lookup_field='username')
    
    class Meta:
        model = User
        field = ('id','username','email','first_name','last_name')
        
class StorySerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    
    def get_validation_exclusions(self):
        exclusions = super(StorySerializer, self).get_validation_exclusions()
        return exclusions + ['author']
    
    class Meta:
        model = Story
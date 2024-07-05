from rest_framework import serializers 
from main.models import users,session,JobDetails,candidate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = session
        fields = '__all__'
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = '__all__'
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = candidate
        fields = '__all__'

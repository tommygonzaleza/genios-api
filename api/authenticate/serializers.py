from django.contrib.auth.models import Group, User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework import serializers

class AuthUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):  
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        return user

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if not email:
            raise serializers.ValidationError('You must provide an email.', code=403)
            
        email = email.lower()
        
        if not username:
            raise serializers.ValidationError('You must provide a username.', code=403)
            
        username = username.lower()
        
        user = User.objects.filter(Q(email__iexact=email) | Q(username=username)).first()
        if user:
            raise serializers.ValidationError('User already exists, please login.', code=403)
        # Add validation for both login and registration if needed
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
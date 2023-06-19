from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializers(serializers.ModelSerializer):
    password= serializers.CharField(max_length=64, min_length=6, write_only=True)  #write only makes sure it is not send to frontend

    class Meta:
        model = User
        fields= ['username', 'email', 'password']

    #validiating the user infornamtin
    def validate(self, attrs):
        email= attrs.get('email','')
        username= attrs.get('username','')
        
        #checking different properties for the validation of username
        if not  username.isalnum():
            
            raise serializers.ValidationError("The username cannot be all numeric")

        return attrs
    
    #this runs after save 
    def create(self, validated_data):

        return User.objects.create_user(**validated_data)  #this invoke create user from the models
    

class EmailVerfificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length= 220)  #priving field for entering the token

    class Meta:
        model= User
        fields=['token']


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255, min_length=2)
    password= serializers.CharField(max_length=80, min_length=6, write_only=True)
    username= serializers.CharField(max_length=200, min_length= 2, read_only= True)
    tokens= serializers.CharField(max_length= 68, min_length=6, read_only= True)

    class Meta:
        model=User
        fields=['email', 'password', 'username', 'tokens']
    #validating the data
    def validate(self, attrs):
        email= attrs.get('email','')
        password= attrs.get('password','')

        #checking for the valid user i.e authentication
        user= auth.authenticate(email=email, password=password)
        #checking differnet parameters
        #if user is not valid
        
        
        
        if not user:
            raise AuthenticationFailed("Invalid Credential, Try Again ")
        
        if not user.is_active:
            raise AuthenticationFailed("Account Disable, Contact Admin")
        
        if not user.is_verified:
            raise AuthenticationFailed("Email is not Verified")

        #returning user details

        return{
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens
        }
        
        
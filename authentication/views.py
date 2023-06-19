from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterSerializers, EmailVerfificationSerializer, LoginSerializer
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .utils import Util
#for getting the domain for sending the email we need to get domain(getting current site)
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse  #takes name of url and give path
import jwt
from django.conf import settings
from rest_framework import views
#creating fields for entering token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RegisterView(generics.GenericAPIView):
    #this helps in accessing the serialized data
    serializer_class= RegisterSerializers

    def post(self, request):
        user= request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)   #is valid method runs the validate method we have created in the registerserializes class
        serializer.save()    #  this method calls the serializers.create method in register serializers
        #returning the data after created
        user_data= serializer.data

        #Now we using token authenticaton
        #first we need to get the user by quering the email
        user= User.objects.get(email= user_data['email'])
        #getting the token
        token= RefreshToken.for_user(user).access_token #for user is the method 
        #calling the util method of util by passing the data
        current_site= get_current_site(request).domain
        #getting the relative link i.e where to redirect the user
        relativeLink= reverse('verifyemail')
        
         #getting protocol
        absurl= 'http://'+ current_site + relativeLink + "?token="+str(token)
        email_body= 'Hi \n'+ user.username +'\n' + 'Use the given link to verify your Email \n'+ absurl
        data= {'email_body':email_body,'email_subject':'Verify Your Email', 'to_email':user.email }
        Util.send_email(data)
        #returning the response
        return Response(user_data, status=status.HTTP_201_CREATED)
    

       
class VerifyEmail(views.APIView):
    serializer_class = EmailVerfificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        #getting the token which was send in the list as in the form of dictionery
        token = request.GET.get('token')
        #decoding the token 
        try:
            payload= jwt.decode(token, settings.SECRET_KEY ,algorithms=["HS256"]) #in payload we decode the user 
            user= User.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified= True
                user.save()
            return Response({'Email':'Email sucessfully activate, Open application for Login'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'Error':'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.DecodeError as identifier:
            return Response({'Error':'Invalid token, Request New One, or Enter Valid One'}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    #user is sending post request
    def post(self, request):
        serializer =self.serializer_class(data= request.data)
        #running valid method in serializer
        serializer.is_valid(raise_exception= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
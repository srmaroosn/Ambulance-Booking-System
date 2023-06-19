from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
#base user manager is the manager of the user whereas abstract base user give the blank template to create the user
class UserManger(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("user should have username")
        if email is None:
            raise TypeError("There should be valid email")
        #creating the user
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("user should have valid password")
        
        #creating the superuser by calling the above function
        user= self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff= True
        user.save()
        return user
        
#now we defining the models for the user

class User(AbstractBaseUser, PermissionsMixin):
    username= models.CharField(max_length=220, unique=True, db_index=True) #db index makes easy in serchingh
    email= models.EmailField(max_length=220, unique=True, db_index=True)
    is_verified= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)  #auto now add help to add created time
    updated_at= models.DateTimeField(auto_now=True)


    #attribute use to login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    #how to manage user
    objects=UserManger()

    def __str__(self):
        return self.email
    

    def tokens(self):
        #creating variables for token for user
        refresh = RefreshToken.for_user(self)

        return{
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }
    

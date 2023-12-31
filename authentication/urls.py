from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.test.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns=[
    
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
    path('register/', RegisterView.as_view(), name="register"),
    path('verifyemail/', VerifyEmail.as_view(), name='verifyemail'),
    path('login/',LoginAPIView.as_view(), name='login' )
]
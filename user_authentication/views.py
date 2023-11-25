from django.shortcuts import render
from .models import User, UserProfile, Token as TK
from .serializers import UserSerializer, UserNullSerializer, LoginSerializer, LogoutSerializer, UserProfileSerializer, TokenSerializer, resetpasswordSerializer
from .utils import hash_password

from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.utils import timezone


class CreateUser(GenericAPIView):
    """
    Create's a normal new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request", request})
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            user.save()
        return Response({
            # "user_id": username.id,
            "data": f"User with {user.email} successfully created"
        })
    

class FetchUsers(ListAPIView):
    """
    Create's a normal new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def check(id):
    try:
        blog = User.objects.get(id=id)
        return blog
    except User.DoesNotExist:
        return Response(status=404)
    
class User_Update(UpdateAPIView):
    #permission_classes = [IsAdminUser]   
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'id'


class User_Retrieve(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'id'

class AddAdminUser(GenericAPIView):
    """
    Gives user admin permission
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserNullSerializer

    def patch(self, request, pk, format=None): # Give specific user admin privilege
        instance = self.get_object()
        if instance is None:
            return Response({"detail": "User with 'ID' does not exist"})
        else:
            instance.is_staff = True
            instance.save()
        return Response({
            "User": instance.email,
            "is_admin": instance.is_staff
        })

class RemoveAdminUser(GenericAPIView):
    """
    Remove user admin permission
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserNullSerializer

    def delete(self, request, pk, format=None): # Remove admin privilege from selected user
        instance = self.get_object()
        if instance is None:
            return Response({"detail": "User with 'ID' does not exist"})
        else:
            instance.is_staff = False
            instance.save()
        return Response({
            "User": instance.email,
            "is_admin": instance.is_staff
        })

# Get all admin user
class AdminUsers(GenericAPIView):
    """
    Returns all admin users in the database
    """
    queryset = User.objects.all()
    serializer_class = UserNullSerializer

    def get(self, request, *args, **kwargs):
        global series # set the global series
        admin_list = list()
        series = 1

        for admin in self.queryset.all():
            if admin.is_staff == True:
                sery = str(series)
                admin_list.append({
                    "user" + sery + "--user_id": admin.id,
                    "user" + sery + "--username": admin.email,
                    "user" + sery + "--is_admin": admin.is_staff,
                })
                int(series)
                series += 1
        return Response({"detail": admin_list})
    
class Login(GenericAPIView):
    serializer_class = LoginSerializer

    @extend_schema(request=serializer_class, responses=serializer_class)
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data['email']).id
            response = serializer.data
            response['user'] = user
            return Response(response,status=status.HTTP_200_OK)

class Logout(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(request=serializer_class, responses=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Response": "Successfully Logged out"}, status=status.HTTP_200_OK)
    
class CreateUserProfile(GenericAPIView):
   
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request", request})
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create(**serializer.validated_data)
            user.save()
        return Response({
            # "user_id": username.id,
            "data": f"Profile for {user.user.email} with USERID={user.user.id} successfully created"
        })

class FetchUserProfile(RetrieveAPIView):
    parser_classes = [FormParser, MultiPartParser, FileUploadParser, JSONParser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer 
    lookup_field = 'id'

class UserProfileUpdate(UpdateAPIView):
    #permission_classes = [IsAdminUser]   
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer 
    lookup_field = 'id'


class CreateToken(GenericAPIView):
   
    queryset = TK.objects.all()
    serializer_class = TokenSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request", request})
        if serializer.is_valid(raise_exception=True):
            token = TK.objects.create(**serializer.validated_data)
            token.save()
            tokenserializer = TokenSerializer(token)
            print(serializer.validated_data)
            return Response({
                # "user_id": username.id,
                "result": f"Token for user with USERID={token.user.id} successfully created",
                "data": tokenserializer.data
                
            })
        return Response({
                "data": serializer.errors
                
            })
        
class resetpassword(GenericAPIView):
   
    queryset = User.objects.all()
    serializer_class = resetpasswordSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request", request})
        userid = User.objects.get(email=request.data['email']).id
        if (TK.objects.get(user__id=userid).expired == False and  timezone.now() > TK.objects.get(user__id=userid).date_created + timezone.timedelta(minutes=5)):
            token = TK.objects.get(user__id=userid)                                                                                                                                                             
            token.expired = True
            return  Response({
                # "user_id": username.id,
                "result": f"Token Expired",
                
            })
        

        elif TK.objects.get(user__id=userid).expired == True:
            token = TK.objects.get(user__id=userid)
            token.delete()
            return  Response({
                # "user_id": username.id,
                "result": f"Token Does not exist",
                
            })
        else: 
            if (TK.objects.filter(user__id=userid).exists() and TK.objects.get(user__id=userid).expired == False) and serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({
                # "user_id": username.id,
                "result": f"User {request.data['email']} Password changed successfully",
                
            })
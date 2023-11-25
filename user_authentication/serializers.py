from rest_framework import serializers
from .models import User, UserProfile, Token
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # user = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    
    class Meta:
        model = UserProfile
        fields =["id", "user", "age", "blood_group", "height", "weight", "genotype", "Medical_records", "date_created", "date_updated"]

class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # images = UserImageSerializer(required=False)
    is_staff = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username','email', 'gender', 'phone_number', 'password', 'lat', 'lon', 'is_staff', 'is_active', 'date_created', 'date_updated']


    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     images_data = request.request.FILES
    #     user = User.objects.create(**validated_data)
    #     for image_data in images_data.values():
    #         UserImages.objects.create(user=user, image=image_data)
    #     return user
    


class UserNullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []

class LoginSerializer(serializers.ModelSerializer):
    user =  serializers.ReadOnlyField()
    email = serializers.CharField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=64, read_only=True)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens', 'user']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        if not user:
            print(user)
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            raise serializers.ValidationError(e)


class resetpasswordSerializer(serializers.ModelSerializer):
    email=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)
    class Meta:
        model=User
        fields= ['email', 'password']
    def save(self):
        email =self.validated_data['email']
        password=self.validated_data['password']
        #filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
        if User.objects.filter(email=email).exists():
        #if your username is existing get the query of your specific username 
            user=User.objects.get(email=email)
            #then set the new password for your username
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error':'please enter valid crendentials'})

class TokenSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    token = serializers.ReadOnlyField()
    expired = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()

    class Meta:
        model = Token
        fields = '__all__'
  
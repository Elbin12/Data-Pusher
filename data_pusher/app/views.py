from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .serializers import SignupSerializer, LoginSerializer, AccountSerializer
from .models import Account

# Create your views here.



class Signup(CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer


class Login(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error':'username and password required.'}, status=400)
        
        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):
                return Response({'error': 'Invalid password'}, status=400)
            
            refresh = RefreshToken()
            refresh['user_id'] = str(user.id)
            refresh["username"] = str(user.username)
            serializer = LoginSerializer(user)
            data = serializer.data
            content = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'userDetails' : data
            }
            return Response({'user_data':content}, status=200)
        except User.DoesNotExist:
            return Response({'error':'Account with this username doesn\'t exist'}, status=400)
            

class AccountView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountList(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountUpdate(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    lookup_field = 'id'
    serializer_class = AccountSerializer


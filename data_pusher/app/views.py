from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .serializers import SignupSerializer, LoginSerializer, AccountSerializer, DestinationSerializer
from .models import Account, Destination

import requests

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
            return Response(content, status=200)
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
    queryset = Account.objects.all().order_by('name')
    serializer_class = AccountSerializer

class AccountUpdate(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    lookup_field = 'id'
    serializer_class = AccountSerializer

class AccountDelete(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    lookup_field = 'id'
    serializer_class = AccountSerializer

class DestinationCreate(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationUpdate(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Destination.objects.all()
    lookup_field = 'id'
    serializer_class = DestinationSerializer

class DestinationDelete(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Destination.objects.all()
    lookup_field = 'id'
    serializer_class = DestinationSerializer

class IncomingData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.headers.get('CL-X-TOKEN')
        if not token:
            return Response({'error':'Un Authenticate'}, status= 400)
        try:
            account = Account.objects.get(app_secret_token=token)
        except:
            return Response({'error':'Invalid token'}, status=403)
        data = request.data
        print('DATA', data)
        for destination in account.destinations.all():
            headers = {
                "APP_ID" : str(account.id),
                "APP_SECRET" : str(account.app_secret_token)
            }
            if destination.http_method == "GET":
                response = requests.get(destination.url, params=data, headers=headers)
            else:
                response = requests.request(destination.http_method, destination.url, json=data, headers=headers)
        return Response({'status':'success'}, status=200)
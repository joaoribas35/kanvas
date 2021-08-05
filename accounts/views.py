from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token

from accounts.serializers import UserSerializer

import ipdb


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error': 'username already exists'}, status=status.HTTP_409_CONFLICT)

        user = User(**serializer.validated_data)

        password = serializer.validated_data['password']

        try:
            validate_password(password, user)
        except ValidationError as e:
            errors = {}

            for arg in e.args[0]:
                errors[arg.code] = arg.messages[0]

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(**serializer.validated_data)

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response({'Unauthorized': 'Failed to authenticate'}, status=status.HTTP_401_UNAUTHORIZED)

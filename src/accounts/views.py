from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import exceptions, status
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .helper import generate_access_token, JWTauthentication

from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def register_view(request, *args, **kwargs):
    data = request.data
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException("Password Does not match")

    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {'data': serializer.data}, 
        status=status.HTTP_201_CREATED
        )

api_view(['POST'])
def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return Response({'Message': 'You are already logged in ...'}, status=400)
    username = request.data.get("username")
    password = request.data.get("password")

    user = (
        User.objects.filter(Q(username__iexact=username)
                            | Q(email__iexact=username))
        .distinct()
        .first()
    )

    if user is None:
        raise exceptions.AuthenticationFailed("user not found")

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Incorrect password")

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {"jwt": token}
    return response


@api_view(["POST"])
def logout_view(request):
    response = Response()
    response.delete_cookie(key="jwt")
    response.data = {"message": "success"}
    return response
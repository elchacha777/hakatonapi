from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer
from .tasks import send_activation_sms

MyUser = get_user_model()

class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered', status=201)


class ActivationView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = MyUser.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)

        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Successfully activated', status=200)
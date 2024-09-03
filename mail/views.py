from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from django import forms
from rest_framework.permissions import AllowAny
import environ
env = environ.Env(
    DEBUG=(bool, False)
)
class ComissionForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    details = forms.CharField(widget=forms.Textarea)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_comission(request):
    form = ComissionForm(request.data)
    # the commssion request emails will be sent to this
    myemail = env('MY_EMAIL')
    if form.is_valid():
        email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        details = form.cleaned_data['details']
        
        try:
            #the email that will be sent to you
            send_mail(
                'Comission Request',
                f'The details provided by the customer: {name} are as follows: {details}',
                settings.EMAIL_HOST_USER,
                [myemail],
                fail_silently=False
            )
            #the email that will be sent to the customer
            send_mail(
                'Comission Request',
                f'hello {name} your request for The commission with these instructions: {details} has been successfully submitted please await our reply',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            return Response({'message': 'Commission request sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)

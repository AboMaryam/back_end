from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER


class OrderView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)

            return Response({
                'data': serializer.data,
                'message': "Orders Data fetche Succesfully"
            }, status=status.HTTP_200_OK)
        
        except:
            
            return Response({
                'data': {},
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                   'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
            
            # Send Email
            subject = " New Order is Pleaced"
            message = "Dear Customer" + " " + data['customer_name'] + "Your order is plased"
            email = data['customer_email']
            recipient_list = [email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)
            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "New order Created Succesfully"
            }, status=status.HTTP_201_CREATED)
        
        except:
            return Response({
                'data': {},
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        try:
            data = request.data
            order1 = Order.objects.filter(id=data.get('id'))
            if not order1.exists():
                return Response({
                    'data': {},
                    'message': "order not found id"
            }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = OrderSerializer(order1[0], data= data, partial=True)

            if not serializer.is_valid():
                return Response({
                'data': serializer.errors,
                'message': "Something went wrong"
                }, status=status.HTTP_500_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "order Updated Succesfully"
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'data': {},
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        try:
            data = request.data
            order1 = Order.objects.filter(id=data.get('id'))

            if not order1.exists():
                return Response({
                    'data': {},
                    'message': "order not found id"
            }, status=status.HTTP_404_NOT_FOUND)

            order1[0].delete()
            return Response({
                'data': {},
                'message': "order Is Deleted"
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'data': {},
                'message': "Something went wrong in Deleting ofthis order"
            }, status=status.HTTP_400_BAD_REQUEST)
        

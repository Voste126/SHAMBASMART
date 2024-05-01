from django.shortcuts import render, get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from . import serializers
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema  

User= get_user_model()
# Create your views here.
class HelloOrdersView (generics.GenericAPIView):
    def get(self,request):
        return Response(data={"message":"Hello Orders"}, status=status.HTTP_200_OK)

class OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='List all orders to the Smart Farm')
    def get(self,request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_description='Create a new order')
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)

        user=request.user
        
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Get a single order')
    def get(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(operation_description='Update a single order')
    def put(self,request,order_id):
        data = request.data
        order= get_object_or_404(Order, pk=order_id)
        serializers = self.serializer_class(data=data,instance=order,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(operation_description='Delete a single order')
    def delete(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(data={"message":"Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UpdateOrderStatusView(generics.GenericAPIView):
    serializer_class = serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    @swagger_auto_schema(operation_description='Update the status of a single order')
    def put(self,request,order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(data=data,instance=order,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#get a user orders based on the user id
class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Get all orders of a single user')
    def get(self,request,user_id):
        user = User.objects.get(pk=request.user.id)
        orders = Order.objects.filter(customer=user)
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
#get a user orders based onthe user id and to a specific order id
class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description='Get a single order of a single user')
    def get(self,request,user_id,order_id):
        try:
            user = User.objects.get(pk=user_id)
            order = Order.objects.filter(customer=user).get(pk=order_id)
            serializer = self.serializer_class(instance=order)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(data={"message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
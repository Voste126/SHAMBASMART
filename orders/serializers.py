from .models import Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=20)
    order_status = serializers.HiddenField(default='PENDING')
    quantity = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = ['id','size', 'order_status', 'quantity']

class OrderDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=20)
    order_status = serializers.CharField(default='PENDING')
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Order
        fields = ['id','size', 'order_status', 'quantity', 'created_at', 'updated_at']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField()
    class Meta:
        model = Order
        fields = ['id','order_status']
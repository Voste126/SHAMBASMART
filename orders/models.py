from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Order(models.Model):
    SIZES=(
        ('SMALL', 'PickupCargo'),
        ('MEDIUM','Mid-TruckCargo'),
        ('LARGE','LorryCargo'),
        ('EXTRA-LARGE','TransistCargo'),
    )
    ORDER_STATUS =(
        ('PENDING','pending'),
        ('ON-TRANSIT','ontransit'),
        ('DeLIVERED','Delivered')
    )
    #one user can have many orders
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    size = models.CharField(max_length=20,choices=SIZES,default = SIZES[0][0])
    order_status = models.CharField(max_length=20,choices=ORDER_STATUS,default = ORDER_STATUS[0][0])
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f'Order size {self.size} by {self.customer}'


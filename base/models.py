from django.db import models
from django.contrib.auth.models import User

class Product(models.Model) :
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='products/', blank=False, null=False)
    stock = models.PositiveIntegerField(default=0)

    
    def __str__(self) :
        
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return self.user.username
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()  
    phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.address}"


class Order(models.Model) :
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.orderitem_set.all())
    
class OrderItem(models.Model) :
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    
    def total_price(self):
        return self.quantity * self.price

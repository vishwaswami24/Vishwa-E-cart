from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Tubelight'),(2,'Fan'),(3,'Bulb'))
    name=models.CharField(max_length=50)
    price=models.FloatField()
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    pdetails=models.CharField(max_length=100,verbose_name="Product Details")
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="image")
    stock=models.IntegerField(default=100)
    brand=models.CharField(max_length=50, default='Generic')

    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0
    
    @property
    def review_count(self):
        return self.review_set.count()
    
class Cart(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')    
    qty=models.IntegerField(default=1)

class Order(models.Model):
    orderid=models.CharField(max_length=50)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')    
    qty=models.IntegerField(default=1)   
    amt=models.FloatField(default=0) 

class OrderHistory(models.Model):
    orderid=models.CharField(max_length=50)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')    
    qty=models.IntegerField(default=1)   
    amt=models.FloatField(default=0)
    date=models.DateTimeField(auto_now_add=True)  
    
class UserInfo(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    gender=models.CharField(max_length=10)
    mobile=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50, default='N/A')
    pincode=models.IntegerField(default=1)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    profile_image=models.ImageField(upload_to="profile_images", blank=True, null=True)
    date_of_birth=models.DateField(blank=True, null=True)

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment=models.TextField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')

class ContactMessage(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.CharField(max_length=20)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)


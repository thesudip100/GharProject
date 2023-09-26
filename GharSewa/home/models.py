from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.

class City(models.Model):
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.city

class Status(models.Model):
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.status
    
class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50)
    service_desc = models.TextField()
    image = models.FileField(null=True)
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.service_name
    

    


    
class userRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    fullAddress = models.CharField(max_length=50)
    profilePic = models.ImageField(upload_to ='customers_pic/',null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName
       

class profRegister(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=CASCADE, null=True, blank=True)
    
    username = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)

    fullAddress = models.CharField(max_length=50)
    profilePic = models.ImageField(upload_to ='prof_pic/',null=True)

    experience=models.IntegerField()
    training_certificate = models.ImageField(upload_to ='training_certificates/',null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName
    

class Booking(models.Model):
    customer = models.ForeignKey(userRegister, on_delete=models.CASCADE, null=True)
    professional = models.ForeignKey(profRegister, on_delete=models.CASCADE, null=True)
    book_date = models.DateField(null=True)
    book_days = models.CharField(max_length=100, null=True)
    book_hours = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.customer.user.first_name + " books "+ self.professional.user.first_name
    

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    content = models.TextField()
    timeStamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message From " + self.name


    


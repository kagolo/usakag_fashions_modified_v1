from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField

# Create your models here.
# staff lib
# from django.core.validators import RegexValidator
# from django.urls import reverse
# from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    number = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price_0 = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    STATUS_TYPE_CHOICES=[
        ('BAGS','BAGS'),
        ('MEN','MEN'),
        ('SCARVES','SCARVES'),
        ('WOMEN','WOMEN')
    ]
    status = models.CharField(max_length=100,choices=STATUS_TYPE_CHOICES)

    STATUS_TYPE_CHOICES=[
        ('YES','YES'),
        ('NO','NO'),
    ]
    special_offers = models.CharField(max_length=100,choices=STATUS_TYPE_CHOICES)

    STATUS_TYPE_CHOICES=[
        ('M','M'),
        ('S','S'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
        ('XXXL','XXXL'),
    ]
    size = models.CharField(max_length=100,choices=STATUS_TYPE_CHOICES)
    
    STATUS_TYPE_CHOICES=[
        ('NEW','NEW'),
        ('SECOND HAND','SECOND HAND'),
    ]
    item_status = models.CharField(max_length=100,choices=STATUS_TYPE_CHOICES)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property 
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity 
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

class Contact_us(models.Model):
    agent_number=models.CharField(max_length=150,null=False,unique=True)
    agent_name=models.CharField(max_length=200,null=False)
    agent_position=models.CharField(max_length=200,null=False)
    agent_contact=models.CharField(max_length=200,null=True)
    agent_image=models.ImageField(upload_to='media')

    def __str__(self):
        return self.agent_name
        

class Carousel(models.Model):
    image_name = models.CharField(max_length=200)
    carousel_image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.image_name

    @property
    def imageURL(self):
        try:
            url = self.carousel_image.url
        except:
            url = ''
        return url


# staff model
# class Student(models.Model):
#     STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

#     GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

#     current_status = models.CharField(
#         max_length=10, choices=STATUS_CHOICES, default="active"
#     )
#     registration_number = models.CharField(max_length=200, unique=True)
#     surname = models.CharField(max_length=200)
#     firstname = models.CharField(max_length=200)
#     other_name = models.CharField(max_length=200, blank=True)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
#     date_of_birth = models.DateField(default=timezone.now)
#     current_class = models.ForeignKey(
#         StudentClass, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     date_of_admission = models.DateField(default=timezone.now)

#     mobile_num_regex = RegexValidator(
#         regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
#     )
#     parent_mobile_number = models.CharField(
#         validators=[mobile_num_regex], max_length=13, blank=True
#     )

#     address = models.TextField(blank=True)
#     others = models.TextField(blank=True)
#     passport = models.ImageField(blank=True, upload_to="students/passports/")

#     class Meta:
#         ordering = ["surname", "firstname", "other_name"]

#     def __str__(self):
#         return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

#     def get_absolute_url(self):
#         return reverse("student-detail", kwargs={"pk": self.pk})
# class StudentBulkUpload(models.Model):
#     date_uploaded = models.DateTimeField(auto_now=True)
#     csv_file = models.FileField(upload_to="students/bulkupload/")



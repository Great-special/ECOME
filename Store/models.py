from django.db import models
from Customer.models import Customer
from django.contrib.auth.models import User

from PIL import Image
from io import BytesIO
from django.core.files import File


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 200, null = True)
    slug = models.SlugField(null=True)
    description = models.TextField(blank = True, null = True)
    price = models.FloatField()
    digital = models.BooleanField(default = True, null = True)
    category = models.ForeignKey('Category', related_name='products', blank = True, on_delete = models.CASCADE, null = True)
    file_name = models.FileField(upload_to='files/', blank = True, null = True)
    image = models.ImageField(upload_to='images/', null=True, blank = True)
    thumbnail = models.ImageField(upload_to='thumbnail/', null=True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True, null=True)
    
    class Meta: # serves as options for the model to select or filter fields
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/"
    
    def get_file_name(self):
        if self.file_name:
            return 'http://127.0.0.1:8000' + self.file_name.url
        return ''
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail

class Category(models.Model):
    name = models.CharField(max_length=200, blank = True, null = True)
    slug = models.SlugField(null=True)
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/{self.slug}/"

class Order(models.Model):
    # A customer can have multiple orders
    user = models.ForeignKey(User, related_name="orders", on_delete = models.SET_NULL, blank = True, null = True)
    date_orderd = models.DateTimeField(auto_now_add = True)
    first_name = models.CharField(max_length = 100, null = True)
    last_name = models.CharField(max_length = 100, null = True)
    email = models.CharField(max_length = 100, null = True)
    address = models.CharField(max_length = 200, null = True)
    zipcode = models.CharField(max_length = 50, null = True)
    place = models.CharField(max_length = 100, null = True)
    phone = models.CharField(max_length = 100, null = True)
    paid_amount = models.DecimalField(max_digits = 8, decimal_places = 2, blank = True, null = True)
    stripe_token = models.CharField(max_length = 100, null = True, blank = True)
    
    class Meta: # serves as options for the model to select or filter fields
        ordering = ('-date_orderd',)
    
    def __str__(self):
        return str(self.first_name)


class OrderItem(models.Model):
    # A single order can have multiple order items
    # A product can have multiple order items
    order = models.ForeignKey(Order, related_name="items", on_delete = models.SET_NULL, null = True, blank = True)
    product = models.ForeignKey(Product, related_name="items", on_delete = models.SET_NULL, null = True, blank = True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank = True, null = True)
    quantity = models.IntegerField(default = 1)
    date_added = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return '%s' % self.id
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    state = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address
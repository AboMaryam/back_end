from django.db import models

# Create your models here.

# The `TimestampModel` class is an abstract model in Python that includes fields for creation and
# update timestamps.
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimestampModel):
    category_name = models.CharField(max_length=100)
    description = models.TextField()
    # category_image = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Product(TimestampModel):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    product_image = models.FileField(upload_to="products/")
    price = models.DecimalField(max_digits =10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Order(TimestampModel):
   customer_name = models.CharField(max_length=100)
#    customer_address = models.CharField(max_length=100, blank=True, null=True)
#    customer_phone = models.CharField(max_length=100, blank=True, null=True)
   customer_email = models.EmailField()
#    total_price = models.DecimalField(max_digits =10, decimal_places=2)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField()

   def __str__(self):
       return f"Order #{self.id}"
    #    return self.customer_name

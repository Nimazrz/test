from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    offer = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.PositiveIntegerField(blank=True)
    weight = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    inventory = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'], name='-created'),
            models.Index(fields=['name'], name='name'),
        ]

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name if self.name else self.image

class ProductFeature(models.Model):
    feature_name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')

    def __str__(self):
        return self.feature_name

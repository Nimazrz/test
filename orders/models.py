from django.db import models
from account.models import ShopUser
from shop.models import Product


# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='buyer', null=False)
    user_first_name = models.CharField(max_length=40)
    user_last_name = models.CharField(max_length=40)
    address = models.TextField(max_length=300)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=10)
    description = models.TextField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=11, )
    email = models.EmailField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 10:
            return 200
        elif 10 <= weight <= 20:
            return 300
        else:
            return 500

    def get_final_cost(self):
        price = self.get_post_cost() + self.get_total_cost()
        return price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField(default=0, )
    quantity = models.PositiveIntegerField(default=1, )
    weight = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity

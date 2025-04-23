from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('tacos', 'Тако'),
        ('burritos', 'Буррито'),
        ('nachos', 'Начос'),
        ('burgers', 'Бургеры'),
        ('sauces', 'Соусы'),
        ('drinks', 'Напитки')
    ]
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='media/dishes/', verbose_name="Изображение")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tacos'
    )
    
    def __str__(self):
        return self.name
        
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def get_total(self):
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    def get_total(self):
            return self.dish.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('preparing', 'Готовится'),
        ('delivering', 'Доставляется'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Наличными'),
        ('card', 'Картой онлайн'),
        ('card_courier', 'Картой курьеру'),
    ]
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='card'
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    def get_total(self):
        return self.price_at_order * self.quantity

# Create your models here.


    
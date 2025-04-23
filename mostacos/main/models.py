from django.db import models

# Create your models here.
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
    image = models.ImageField(upload_to='dishes/', verbose_name="Изображение")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tacos'
    )
    
    def __str__(self):
        return self.name
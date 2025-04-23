from django.shortcuts import render
from main.models import Dish

def index(request):
    categories = {
        'tacos': Dish.objects.filter(category='tacos')[:3],
        'burritos': Dish.objects.filter(category='burritos')[:3],
        'nachos': Dish.objects.filter(category='nachos')[:3],
        'burgers': Dish.objects.filter(category='burgers')[:3],
        'sauces': Dish.objects.filter(category='sauces')[:3],
        'drinks': Dish.objects.filter(category='drinks')[:3],
    }
    return render(request, 'main/index.html', categories)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderForm
from main.models import Dish
from django.http import JsonResponse



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'main/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'"{dish.name}" добавлен в корзину'})
    
    messages.success(request, f'"{dish.name}" добавлен в корзину')
    return redirect('index')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Блюдо удалено из корзины')
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем заказ
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'pending'  # Устанавливаем начальный статус
            order.total_price = sum(item.dish.price * item.quantity for item in cart.items.all())
            order.save()  # Сохраняем заказ в БД
            
            # Переносим товары из корзины в заказ
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    dish=cart_item.dish,
                    quantity=cart_item.quantity,
                    price_at_order=cart_item.dish.price  # Фиксируем цену на момент заказа
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'main/checkout.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Получаем все заказы пользователя, отсортированные по дате создания
    user_orders = Order.objects.filter(user=request.user).order_by('created_at')
    
    # Получаем список ID заказов для поиска позиции текущего заказа
    order_ids = list(user_orders.values_list('id', flat=True))
    
    # Находим порядковый номер текущего заказа (начиная с 1)
    order_number = order_ids.index(order.id) + 1
    
    return render(request, 'main/details.html', {
        'order': order,
        'order_number': order_number,
        'total_orders': len(order_ids)  # Общее количество заказов пользователя
    })




def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


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


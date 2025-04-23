from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from main.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish', 'quantity', 'price_at_order', 'get_total')
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сумма'


admin.site.register(User)

class CustomUserAdmin(UserAdmin):
    # Добавляем новую вкладку в детальном просмотре пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('История заказов', {'fields': ()}),  # Пустые fields, так как используем метод
    )
    
    # Метод для отображения ссылки на заказы
    def orders_link(self, obj):
        count = obj.orders.count()  # Используем related_name 'orders'
        url = reverse('admin:main_order_changelist') + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">Просмотреть заказы ({})</a>', url, count)
    orders_link.short_description = 'История заказов'
    
    # Добавляем поле в список display
    list_display = UserAdmin.list_display + ('orders_link',)
    
    # Добавляем метод в readonly_fields
    readonly_fields = ('orders_link',)

# Регистрируем кастомный админ-класс
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.unregister(User)  # Сначала анрегистрируем стандартный
admin.site.register(User, CustomUserAdmin)


from django import forms
from .models import Order, CartItem

class OrderForm(forms.ModelForm):
    # Добавляем поле для способа оплаты (не из модели)
    PAYMENT_CHOICES = [
        ('cash', 'Наличными при получении'),
        ('card', 'Картой онлайн'),
        ('card_courier', 'Картой курьеру'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Способ оплаты',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='card'  # Значение по умолчанию
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'phone']
        labels = {
            'delivery_address': 'Адрес доставки',
            'phone': 'Телефон'
        }
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Улица, дом, квартира',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX',
                'required': True
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.startswith('+7'):
            raise forms.ValidationError("Номер должен начинаться с +7")
        if len(phone) < 11:
            raise forms.ValidationError("Номер слишком короткий")
        return phone

    def save(self, commit=True):
        # Сохраняем payment_method в экземпляр модели
        order = super().save(commit=False)
        order.payment_method = self.cleaned_data['payment_method']
        if commit:
            order.save()
        return order
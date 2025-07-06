from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Architect, Store, Sale

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 
                 'is_architect', 'is_store_admin', 'allowed_stores')

class ArchitectForm(forms.ModelForm):
    class Meta:
        model = Architect
        fields = '__all__'
        ##exclude = ('user',)

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('architect','store', 'value', 'date', 'cpf', 'nota_fiscal')
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'text',        # Isso é necessário para o Flatpickr funcionar
                'id': 'datepicker',    # O seletor que usaremos no JS
                'class': 'form-control',
                'style': 'max-width: 110px;',
                'placeholder': 'Selecione uma data',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SaleForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['architect'].queryset = Architect.objects.all()
            if not user.is_superuser:
                self.fields['architect'].queryset = Architect.objects.filter(
                    user__allowed_stores__in=user.allowed_stores.all()
                ).distinct()
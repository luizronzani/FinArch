from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Architect, Store, Sale, UserStore
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from dal import autocomplete


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_store_admin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Usuário', css_class='btn-primary'))


class ArchitectForm(forms.ModelForm):
    class Meta:
        model = Architect
        fields = ['name', 'cpf_cnpj', 'registration_number', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Arquiteto', css_class='btn-primary'))

class UserStoreForm(forms.ModelForm):
    class Meta:
        model = UserStore
        fields = ['user', 'store']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Ligação', css_class='btn-primary'))

class UserStoreFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        label='Usuário',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        required=False,
        label='Loja',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'cnpj', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Loja', css_class='btn-primary'))


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('architect', 'store', 'value', 'date', 'cpf_cnpj', 'nota_fiscal')
        widgets = {
            'architect': autocomplete.ModelSelect2(url='architect-autocomplete'),
            'store': autocomplete.ModelSelect2(url='store-autocomplete'),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'id': 'datepicker',
                'class': 'form-control',
                'style': 'max-width: 110px;',
                'placeholder': 'Data',
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF ou CNPJ sem pontos',
                'maxlength': 14,
            }),
            'nota_fiscal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da Nota Fiscal',
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
        }
        labels = {
            'architect': 'Arquiteto',
            'store': 'Loja',
            'value': 'Valor da Venda',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and not self.user.is_superuser:
            lojas_user = UserStore.objects.filter(user=self.user).values_list('store', flat=True)
            self.fields['store'].queryset = Store.objects.filter(id__in=lojas_user)

        self.fields['architect'].queryset = self.fields['architect'].queryset.filter(is_active=True)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar Venda', css_class='btn-primary'))

    def clean_store(self):
        store = self.cleaned_data.get('store')
        user = self.user

        if store and user and not user.is_superuser:
            if not UserStore.objects.filter(user=user, store=store).exists():
                raise forms.ValidationError("Você não tem permissão para registrar vendas nesta loja.")
        return store

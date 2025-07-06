from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Architect, Store, Sale, UserStore


# Customização do admin de usuário
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_store_admin', 'is_active')
    list_filter = ('is_store_admin', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('is_store_admin',)}),
    )


# Exibir campos úteis no admin de Architect
class ArchitectAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf_cnpj', 'registration_number', 'is_active', 'created_at')
    search_fields = ('name', 'cpf_cnpj')
    list_filter = ('is_active',)


# Exibir campos úteis no admin de Store
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'address', 'is_active', 'created_at')
    search_fields = ('name', 'cnpj')
    list_filter = ('is_active',)


# Exibir vendas com informações importantes
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'architect', 'store', 'value', 'date', 'nota_fiscal', 'created_by')
    search_fields = ('nota_fiscal', 'cpf_cnpj')
    list_filter = ('store', 'architect', 'date')


# Exibir associações entre usuários e lojas
class UserStoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'created_at')
    list_filter = ('store',)


# Registro de todos os modelos
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Architect, ArchitectAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(UserStore, UserStoreAdmin)

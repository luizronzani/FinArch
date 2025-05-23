from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Architect, Store, Sale

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_architect', 'is_store_admin')
    list_filter = ('is_staff', 'is_architect', 'is_store_admin')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_architect', 'is_store_admin', 'allowed_stores')}),
    )
    filter_horizontal = ('allowed_stores',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Architect)
admin.site.register(Store)
admin.site.register(Sale)
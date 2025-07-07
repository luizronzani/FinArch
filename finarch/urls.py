from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import ArchitectAutocomplete, StoreAutocomplete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('architect-autocomplete/', ArchitectAutocomplete.as_view(), name='architect-autocomplete'),
    path('store-autocomplete/', StoreAutocomplete.as_view(), name='store-autocomplete'),
    path('', include('core.urls')),
    path('accounts/', include([
        path('login/', auth_views.LoginView.as_view(), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    ])),
]


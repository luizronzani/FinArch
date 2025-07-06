from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import CustomUser, Architect, Store, Sale, UserStore
from .forms import CustomUserCreationForm, ArchitectForm, StoreForm, SaleForm
from dal import autocomplete

class ArchitectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Architect.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class StoreAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Store.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


def is_store_user(user):
    # Verifica se usuário está autenticado e tem lojas associadas via UserStore
    return user.is_authenticated and UserStore.objects.filter(user=user).exists()

@staff_member_required
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register_user.html', {'form': form})

@staff_member_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

@staff_member_required
def register_architect(request):
    if request.method == 'POST':
        form = ArchitectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('architect_list')
    else:
        form = ArchitectForm()
    return render(request, 'core/register_architect.html', {'form': form})

@staff_member_required
def architect_list(request):
    architects = Architect.objects.all()
    return render(request, 'core/architect_list.html', {'architects': architects})

@staff_member_required
def register_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_list')
    else:
        form = StoreForm()
    return render(request, 'core/register_store.html', {'form': form})

@staff_member_required
def store_list(request):
    stores = Store.objects.all()
    return render(request, 'core/store_list.html', {'stores': stores})

@login_required
@user_passes_test(is_store_user)
def register_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, user=request.user)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            # Se quiser limitar a loja para a primeira associada do usuário, descomente:
            # user_stores = UserStore.objects.filter(user=request.user)
            # if user_stores.exists():
            #     sale.store = user_stores.first().store
            sale.save()
            return redirect('sale_list')
    else:
        form = SaleForm(user=request.user)
    return render(request, 'core/register_sale.html', {'form': form})

@login_required
def sale_list(request):
    if request.user.is_superuser:
        sales = Sale.objects.all()
    else:
        # Buscar lojas associadas via UserStore
        user_stores = UserStore.objects.filter(user=request.user).values_list('store', flat=True)
        sales = Sale.objects.filter(store__in=user_stores)
    return render(request, 'core/sale_list.html', {'sales': sales})

def landing_page(request):
    return render(request, 'core/landing.html')

@login_required
def report(request):
    if request.user.is_superuser:
        sales = Sale.objects.all()
    else:
        user_stores = UserStore.objects.filter(user=request.user).values_list('store', flat=True)
        sales = Sale.objects.filter(store__in=user_stores)
    return render(request, 'core/report/report.html', {'sales': sales})

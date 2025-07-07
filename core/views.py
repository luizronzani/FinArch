from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import CustomUser, Architect, Store, Sale, UserStore
from .forms import CustomUserCreationForm, ArchitectForm, StoreForm, SaleForm, UserStoreFilterForm, UserStoreForm
from dal import autocomplete
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse

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
def register_user_store(request):
    if request.method == 'POST':
        form = UserStoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_store_filter')  # ou outra URL após cadastro
    else:
        form = UserStoreForm()
    return render(request, 'core/register_user_store.html', {'form': form})

@staff_member_required
def delete_user_store(request, pk):
    relation = get_object_or_404(UserStore, pk=pk)
    relation.delete()
    return redirect('user_store_filter')  # ajuste para o nome da URL da listagem

@staff_member_required
def user_store(request):
    user_store = Architect.objects.all()
    return render(request, 'core/user_store.html', {'user_store': user_store})

@staff_member_required
def user_store_filter(request):
    form = UserStoreFilterForm(request.GET or None)
    user_store = UserStore.objects.select_related('user', 'store')

    if form.is_valid():
        user = form.cleaned_data.get('user')
        store = form.cleaned_data.get('store')

        if user:
            user_store = user_store.filter(user=user)
        if store:
            user_store = user_store.filter(store=store)

    return render(request, 'core/user_store_filter.html', {
        'form': form,
        'user_store': user_store,
    })

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
        # Pega apenas as lojas associadas ao usuário
        lojas_user = UserStore.objects.filter(user=request.user).values_list('store', flat=True)
        sales = Sale.objects.filter(store__in=lojas_user)

    return render(request, 'core/sale_list.html', {'sales': sales})

def landing_page(request):
    return render(request, 'core/landing.html')

@login_required
def sales_ajax(request):
    user = request.user
    user_stores = user.userstore_set.values_list('store', flat=True)

    sales = Sale.objects.filter(store__in=user_stores).select_related('architect', 'store')

    data = []
    for sale in sales:
        data.append({
            'architect': sale.architect.name,
            'date': sale.date.strftime('%d/%m/%Y'),
            'nota_fiscal': sale.nota_fiscal,
            'store': sale.store.name,
            'value': f"{sale.value:.2f}",
        })

    return JsonResponse({'data': data})

########################################
############# RELATORIOS# #############
########################################


@login_required
def relatorios(request):
    user = request.user
    ano_atual = datetime.now().year

    # Lista de lojas que o usuário tem ligação
    lojas_user = UserStore.objects.filter(user=user).values_list('store', flat=True)

    # Filtra lojas para mostrar no filtro
    lojas_disponiveis = Store.objects.filter(id__in=lojas_user)

    # Pega loja selecionada no filtro (GET)
    loja_selecionada = request.GET.get('store')

    # Base queryset: só vendas nas lojas do usuário
    vendas = Sale.objects.filter(store__in=lojas_user, date__year=ano_atual)

    # Se o usuário selecionou uma loja no filtro, filtra por ela também
    if loja_selecionada:
        vendas = vendas.filter(store_id=loja_selecionada)

    # Agrupamento por mês para o gráfico mensal
    vendas_por_mes = vendas.annotate(mes=ExtractMonth('date')) \
                          .values('mes') \
                          .annotate(total=Sum('value')) \
                          .order_by('mes')

    # Total do ano para gráfico geral
    total_ano = vendas.aggregate(total=Sum('value'))['total'] or 0

    context = {
        'vendas_por_mes': vendas_por_mes,
        'total_ano': total_ano,
        'lojas': lojas_disponiveis,
        'loja_selecionada': int(loja_selecionada) if loja_selecionada else None,
    }
    return render(request, 'core/relatorios.html', context)



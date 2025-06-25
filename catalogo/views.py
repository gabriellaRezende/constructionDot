from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from catalogo.forms import ProdutoForm
from catalogo.models import Produto 

# Create your views here.

@login_required
def produto_list(request):
    qs = Produto.objects.filter(fornecedor=request.user.suplier_profile)
    return render(request, 'supplier/produto_list.html', {'products': qs})

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.fornecedor = request.user.suplier_profile
            produto.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm()
    return render(request, 'supplier/produto_form.html', {'form': form})

@login_required
def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk, fornecedor=request.user.suplier_profile)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_list')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'supplier/produto_form.html', {'form': form})

@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk, fornecedor=request.user.suplier_profile)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'supplier/produto_confirm_delete.html', {'object': produto})
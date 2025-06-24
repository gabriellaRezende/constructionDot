from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def group_required(group_name):
    def in_group(u):
        if u.is_authenticated:
            if u.groups.filter(name=group_name).exists() or u.is_staff:
                return True
        return False
    return user_passes_test(in_group, login_url='/sem-permissao/')

def supplier_required(view_func):
    return group_required('Fornecedor')(view_func)

def client_required(view_func):
    return group_required('Cliente')(view_func)
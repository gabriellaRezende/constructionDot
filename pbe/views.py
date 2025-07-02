# views.py
from oscar.apps.basket.views import BasketAddView
from oscar.core.loading import get_model
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.apps import apps

Basket = get_model('basket', 'Basket')
Line = get_model('basket', 'Line')
StockRecord = get_model('partner', 'StockRecord')
Product = get_model('catalogue', 'Product')


class CustomAddToBasketView(BasketAddView):

    def get_product(self, request):
        """
        Aqui vamos buscar o stockrecord_id enviado pelo formulário
        """
        stockrecord_id = request.POST.get('stockrecord_id')
        if stockrecord_id:
            stockrecord = get_object_or_404(StockRecord, id=stockrecord_id)
            return stockrecord.product
        return super().get_product(request)

    def get_form_kwargs(self):
        """
        Passa o stockrecord_id para o form
        """
        kwargs = super().get_form_kwargs()
        kwargs['stockrecord_id'] = self.request.POST.get('stockrecord_id')
        return kwargs

    def form_valid(self, form):
        stockrecord_id = self.request.POST.get('stockrecord_id')
        print(f"StockRecord ID recebido: {stockrecord_id}") # Debugging line
        if stockrecord_id:
            stockrecord = get_object_or_404(StockRecord, id=stockrecord_id)
            quantity = form.cleaned_data['quantity']
            self.request.basket.add_product(
                stockrecord.product,
                quantity=quantity,
                stockrecord=stockrecord
            )
            return self.get_success_url_response()
        return super().form_valid(form)



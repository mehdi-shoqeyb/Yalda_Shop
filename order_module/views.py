from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest
from order_module.models import Order
from product_module.models import Product
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required,name='dispatch')  
class OrderView(View):
    def get(self,request:HttpRequest):
        order = Order.objects.prefetch_related('order_products').filter(user=request.user,is_paid=False).first()
        context = {
            'order':order,
        }
        return render(request,'order_module/basket.html',context)
    
    def post(self,request:HttpRequest):
        context = {
            
        }
        return render(request,'order_module/basket.html',context)
  
login_required
def delete_from_basket(request:HttpRequest,product_id):
    product = Product.objects.filter(id=product_id).first()
    order = Order.objects.filter(user=request.user,is_paid=False).first()
    order_item = order.order_products.get(product=product)
    order_item.delete()
    return redirect(reverse('user-basket'))

login_required
def delete_all_from_basket(request:HttpRequest):
    order = Order.objects.filter(user=request.user,is_paid=False).first()
    order_item = order.order_products.all()
    order_item.delete()
    return redirect(reverse('user-basket'))
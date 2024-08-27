from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.db.models import Prefetch
from product_module.models import Product,ProductBrand,ProductCategory,PriceFilter,ProductTag
from order_module.models import Order
from django.utils import timezone

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs) 
        context['categories'] = ProductCategory.objects.filter(is_active=True).all()[:8]
        context['amazing_offers'] = Product.objects.filter(is_active=True,discount_expiry__gt=timezone.now()).order_by('-discount_percent')[:8]
        context['mobiles'] = Product.objects.filter(is_active=True,category__url_title__iexact='mobile')[:8]
        context['price_filters'] = PriceFilter.objects.filter(is_active=True,).all()
        context['latest_products'] = Product.objects.filter(is_active=True,).order_by('-id')[:8]
        return context

class ContactUs(View):
    def get(self,request):
        context ={
            
        }
        return render(request,'home_module/contact-us.html',context)

def site_header_component(request):
    if request.user.is_authenticated:
        order = Order.objects.prefetch_related('order_products').filter(user=request.user,is_paid=False).first()     
        if order is not None:
            order_products_count = order.order_products.count()
        else:
            order_products_count = 0
            
        context = {
        'order':order,
        'products_count':order_products_count,
        }
    else:
        context ={
            
        }
        
    return render(request, 'shared/site_header_component.html', context)

def site_mega_menu_component(request):
    categories = ProductCategory.objects.filter(is_active=True).prefetch_related('tag_categories')
    categories = categories.prefetch_related('brands_categories')
    
    price_filters = PriceFilter.objects.all()
    
    context = {
        'categories':categories,
        'price_filters':price_filters,
    }
    return render(request, 'shared/site_mega_menu_component.html', context)


def site_footer_component(request):
    if request.user.is_authenticated:
        order = Order.objects.prefetch_related('order_products').filter(user=request.user,is_paid=False).first()     
        if order is not None:
            order_products_count = order.order_products.count()
        else:
            order_products_count = 0
            
        context = {
        'order':order,
        'products_count':order_products_count,
        }
    else:
        context ={
            
        }
        
    return render(request, 'shared/site_footer_component.html', context)

   
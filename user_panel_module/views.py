from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView,View,DetailView
from django.http import HttpRequest
from account_module.models import User
from product_module.models import Product
from .forms import ProfilePictureModelForm,UserInformationModelForm,ChangePasswordForm
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from order_module.models import Order
  
@method_decorator(login_required,name='dispatch')  
class CounterPage(ListView):
    template_name = 'user_panel_module/counter.html'
    model = Order
    context_object_name = 'orders'
    ordering = ['-order_date']
    paginate_by = 4

    def get_queryset(self):
        return Order.objects.prefetch_related('order_products').filter(is_paid=True).order_by(*self.ordering)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CounterPage,self).get_context_data()
        context['favorites'] = self.request.user.favorite_products.all()[:4]
        return context
        
@method_decorator(login_required,name='dispatch')  
class InformationPage(View):
    def get(self,request:HttpRequest):
        user = User.objects.filter(id=request.user.id).first()
        info_form = UserInformationModelForm(instance=user)
        picture_form = ProfilePictureModelForm(instance=user)
        context = {
            'user': user,
            'picture_form':picture_form,
            'info_form':info_form
        }
        return render(request,'user_panel_module/user-info.html',context)
    
    def post(self,request:HttpRequest):
        user = User.objects.filter(id=request.user.id).first()
        if 'profile_picture' in request.FILES: 
            picture_form = ProfilePictureModelForm(request.POST,request.FILES,instance=user)
            if picture_form.is_valid():
                picture_form.save()
                return redirect(reverse('user-panel-info'))
            else:
                picture_form.add_error('profile_picture','عکس ارسال نشد')
                info_form = UserInformationModelForm(instance=user)
                context = {
                    'user': user,
                    'picture_form':picture_form,
                    'info_form':info_form
                }
                return render(request,'user_panel_module/user-info.html',context)
        else:
            info_form = UserInformationModelForm(request.POST,instance=user)
            print(info_form)
            if info_form.is_valid():
                info_form.save()
                return redirect(reverse('user-panel-info'))
            else:
                picture_form = ProfilePictureModelForm(request.POST,request.FILES,instance=user)
                context = {
                    'user': user,
                    'picture_form':picture_form,
                    'info_form':info_form
                }
                return render(request,'user_panel_module/user-info.html',context)

@method_decorator(login_required,name='dispatch')     
class LastOrdersView(ListView):
    template_name = 'user_panel_module/last-orders.html'
    model = Order
    context_object_name = 'orders'
    ordering = ['-order_date']
    paginate_by = 4

    def get_queryset(self):
        return Order.objects.prefetch_related('order_products').filter(is_paid=True).order_by(*self.ordering)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LastOrdersView,self).get_context_data()
        return context

class OrderDetailView(DetailView):
    template_name = 'user_panel_module/order-detail.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  

@method_decorator(login_required,name='dispatch')           
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        forms = ChangePasswordForm()
        print(request.user)
        context = {
            'forms': forms
        }
        return render(request, 'user_panel_module/change-password.html', context)

    def post(self, request: HttpRequest):
        forms = ChangePasswordForm(request.POST)
        if forms.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(forms.cleaned_data.get('current_password')):
                if not current_user.check_password(forms.cleaned_data.get('password')):
                    current_user.set_password(forms.cleaned_data.get('password'))
                    current_user.save()
                    logout(request)
                    return redirect(reverse('login-page'))
                else:
                    forms.add_error('password', 'رمز عبور جدید و قبلی یکی می باشد')
            else:
                forms.add_error('current_password', 'رمز عبور قبلی اشتباه می باشد')
        context = {
            'forms': forms,
        }
        return render(request, 'user_panel_module/change-password.html', context)
    
@method_decorator(login_required,name='dispatch')  
class FavoriteProductsPage(ListView):
    template_name = 'user_panel_module/favorite-products.html'
    model = Product
    paginate_by = 4
    
    def get_queryset(self):
        return self.request.user.favorite_products.all()
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteProductsPage,self).get_context_data(object_list=object_list, **kwargs)     
        context['favorites'] = context['object_list']
        return context
    
    def post(self,request):
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        self.request.user.favorite_products.remove(product)
        return redirect(reverse('user-panel-favorite-products'))
     
class OrderFactorView(DetailView):
    template_name = 'user_panel_module/factor.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_products_count = self.object.order_products.count()
        context['order_products_count'] =order_products_count
        context['total_price_with_delivery'] = order_products_count + self.object.delivery_price
        return context  
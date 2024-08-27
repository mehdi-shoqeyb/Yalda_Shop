from django.views.generic import ListView,DetailView
from .models import Product,ProductTag,ProductCategory,ProductGallery,ProductQuestionsAnswers,ProductComment
from django.http import HttpRequest,JsonResponse
from django.db import models
from utils.convertors import extract_values_to_string,comment_rates,comment_rates_percentages
from django.utils import timezone
from order_module.models import Order,OrderItem
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
class ProductListView(ListView):
    template_name = 'product_module/products-list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 9
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView,self).get_context_data()
        request : HttpRequest = self.request
        context['categories'] =ProductCategory.objects.filter(is_active=True)

        current_cat = self.kwargs.get('cat')
        context['tags'] = ProductTag.objects.filter(is_parent=False,category__isnull=False,category__url_title__iexact=current_cat
            ).annotate(
                product_count=models.Count('products_tag', filter=models.Q(products_tag__category__url_title=current_cat))
            ).distinct()
            
        context['selected_tags'] = request.GET.getlist('tags')
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        sort = request.GET.get('sort')
        context['db_max_price'] = db_max_price
        context['start_price'] = request.GET.get('start_price') or 0
        context['end_price'] = request.GET.get('end_price') or db_max_price
        return context
    
    def get_queryset(self):
        query = super(ProductListView,self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request : HttpRequest = self.request
        sort = request.GET.get('sort')
        search_query = request.GET.get('search', '')
        end_price = request.GET.get('end_price')
        start_price = request.GET.get('start_price')

        if search_query:
            query = query.filter(models.Q(title__icontains=search_query))

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        selected_tags = request.GET.getlist('tags')
        
        if selected_tags:
            query = query.filter(tags__url_title__in=selected_tags).distinct()
        
        if sort is not None:
            if sort == 'discounts':
                query = query.filter(discount_percent__gt=0, discount_expiry__gt=timezone.now()).order_by('-discount_percent')
            else:
                query = query.order_by(sort)
            
        if start_price is not None: 
            query = query.filter(price__gte=start_price) 
            
        if end_price is not None: 
            query = query.filter(price__lte=end_price)
            
        return query

class ProductDetailView(DetailView):
    template_name = 'product_module/product-detail.html'
    model = Product
    
    def get_context_data(self, **kwargs):
        # product content
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        
        galleries = list(loaded_product.product_images.all())
        galleries.insert(0,loaded_product)
        context['product_galleries'] = galleries
        
        features = loaded_product.get_features()
        features = {k: features[k] for k in list(features.keys())[:3]}
        context['features'] = features
        
        # product qustion and answers setion
        context['questions'] = ProductQuestionsAnswers.objects.filter(
            product_id=loaded_product.id, parent=None
        ).annotate(
            answers_count=models.Count('question_answers')
        ).prefetch_related('question_answers')
        context['QAA_total_count'] =  ProductQuestionsAnswers.objects.filter(product_id=loaded_product.id).count()
        
        #  product comment section sort
        comments = ProductComment.objects.filter(product=loaded_product)
        rates_detail = comment_rates(comments)
        context['rates_detail'] = rates_detail
        context['rates_percentages'] = comment_rates_percentages(rates_detail)
          
        sort = self.request.GET.get('sort')
        if sort is not None:
            if sort == 'buyer':
                comments = comments.filter(buyer=True)
            else:
                comments = comments.order_by(sort)
                
        context['comments'] = comments
        comments_count = comments.count()
        context['comments_count'] =comments_count
        
        # realated products 
        context['realated_proucts'] = Product.objects.filter(is_active=True,brand=loaded_product.brand).exclude(id=loaded_product.id)[:10]
        if self.request.user.is_authenticated:
            context['favorite_exists'] = self.request.user.favorite_products.filter(id=loaded_product.id).exists()
            
        return context
        
def QustionAndAnswers(request:HttpRequest):
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        text = request.POST.get('text')
        product_id = request.POST.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        
        new_QAA = ProductQuestionsAnswers(
            user= request.user,
            text = text,    
            product=product
        )
        
        if parent_id:
            parent = ProductQuestionsAnswers.objects.filter(id=parent_id).first()
            new_QAA.parent = parent
            
        new_QAA.save()
        
        return JsonResponse({'success': True, 'message': 'Question or answer added successfully'})

def NewComment(request:HttpRequest): 
    if request.method == 'POST':
        product_id = request.POST.get('product_id')           
        rate = request.POST.get('rating')
        comment = request.POST.get('comment-text')
        pros_dict = request.POST.get('tags-pos') or None
        cons_dict = request.POST.get('tags-neg') or None
        
        product = Product.objects.get(id=product_id)
        
        new_comment = ProductComment(
            product = product,
            user = request.user,
            comment = comment,
            rate = rate,
        )
        
        if pros_dict is not None:
            pros = extract_values_to_string(pros_dict)
            new_comment.pros = pros

        if cons_dict is not None:
            cons = extract_values_to_string(cons_dict)
            new_comment.cons = cons
        
        new_comment.save()
        
        comments= ProductComment.objects.filter(product=product)
        # product rate
        product_rate = comments.aggregate(models.Avg('rate'))['rate__avg'] or 0
        if round(product_rate, 1) > 5:
            product.rate = 5
        product.rate = round(product_rate, 1)
        # product satisfaction_percentage
        comments_count = comments.count()
        satisfied_comments = ProductComment.objects.filter(rate__gte=4).count()
        
        if comments_count == 0:
            satisfaction_percentage =0.0
            
        # Calculate satisfaction percentage
        satisfaction_percentage = (satisfied_comments / comments_count) * 100
        product.satisfaction = round(satisfaction_percentage, 2)
        product.save()
        return JsonResponse({'success': True, 'message': 'comment aded successfully'})

def comment_likes_and_dislikes(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_id = request.POST.get('comment_id')
            opinion = request.POST.get('opinion')
            comment = ProductComment.objects.get(id=comment_id)
            
            if opinion == 'like':
                if request.user in comment.likes.all():
                    comment.likes.remove(request.user)
                    return JsonResponse({
                    'status': 'success',
                    'total_likes': comment.total_likes(),
                    'total_dislikes': comment.total_dislikes()
                    })
                else:
                    comment.likes.add(request.user)
                    comment.dislikes.remove(request.user)
                    
                    return JsonResponse({
                    'status': 'success',
                    'total_likes': comment.total_likes(),
                    'total_dislikes': comment.total_dislikes()
                    })

            elif opinion == 'dislike':
                if request.user in comment.dislikes.all():
                    comment.dislikes.remove(request.user)
                    return JsonResponse({
                    'status': 'success',
                    'total_likes': comment.total_likes(),
                    'total_dislikes': comment.total_dislikes()
                    })
                else:
                    comment.dislikes.add(request.user)
                    comment.likes.remove(request.user)
                    
                    return JsonResponse({
                    'status': 'success',
                    'total_likes': comment.total_likes(),
                    'total_dislikes': comment.total_dislikes()
                    })
        else:
            return JsonResponse({
                    'status': 'error',
                    'message':'برای ثبت نظر باید به حساب کاربری خود وارد شوید'
                    })
            
def add_product_to_favorite(request:HttpRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('favorite-product-id')
            product = Product.objects.filter(id=product_id).first()
            favorite_exists = request.user.favorite_products.filter(id=product_id).exists()
                
            if favorite_exists:
                request.user.favorite_products.remove(product)
                return redirect(reverse('product-detail', kwargs={'slug': product.slug}))
            else:
                request.user.favorite_products.add(product)
                return redirect(reverse('product-detail', kwargs={'slug': product.slug})) 
        else:
            pass
        
        
def add_product_to_basket(request:HttpRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            product_color = request.POST.get('color')
            product_count = int(request.POST.get('count', 1))
            product = Product.objects.filter(id=product_id).first()
            order = Order.objects.prefetch_related('order_products').filter(user=request.user,is_paid=False).first()
            if order is None:
                order = Order(
                    user=request.user,
                    is_paid=False,
                )
                order.save()
            
            order_item= OrderItem.objects.filter(order=order,product=product).first()
            if order_item:
                order_item.count += product_count
                order_item.color = product_color
                order_item.save()
            else:
                order_item = OrderItem(
                    order=order,
                    product=product,
                    color=product_color,
                    count=product_count
                )
                order_item.save()
            
            return JsonResponse({'success':'محصول به سبد خرید اضافه شد'})         
        return JsonResponse({'failed':'برای افزودن محصول به سبد خرید باید وارد حساب کاربری شوید '})
        
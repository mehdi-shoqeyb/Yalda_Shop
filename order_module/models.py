from django.db import models
import uuid

class DiscountCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='کد تخفیف')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='مقدار تخفیف')
    valid_from = models.DateTimeField(verbose_name='تاریخ اعتبار از')
    valid_to = models.DateTimeField(verbose_name='تاریخ اعتبار تا')

    def valid_discount_code(self):
        if self.valid_from < self.valid_to:
            return True
        return False

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return self.code
    
class Order(models.Model):
    user = models.ForeignKey('account_module.User', on_delete=models.CASCADE, verbose_name='کاربر')
    order_code = models.UUIDField(null=True,blank=True,editable=False, unique=True, verbose_name='کد پیگیری سفارش')
    order_date = models.DateField(null=True,blank=True,verbose_name='تاریخ ثبت سفارش')
    recipient_name = models.CharField(null=True,blank=True,max_length=100, verbose_name='تحویل گیرنده')
    recipient_phone = models.CharField(null=True,blank=True,max_length=15, verbose_name='شماره موبایل')
    address = models.TextField(null=True,blank=True,verbose_name='آدرس')
    final_price = models.IntegerField(null=True,blank=True,verbose_name='مبلغ نهایی')
    discount_code = models.ForeignKey('DiscountCode', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='کد تخفیف')
    delivery_date = models.DateField(null=True,blank=True,verbose_name='تاریخ تحویل')
    delivery_time_range = models.CharField(null=True,blank=True,max_length=50, verbose_name='زمان تحویل')
    delivery_price = models.IntegerField(null=True,blank=True,verbose_name='هزینه ارسال')
    is_paid = models.BooleanField(default=False,verbose_name='نهایی شده / نشده')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return f'Order {self.order_code} by {self.user}'
    
    # get the product price by count
    def get_products_total_price(self):
        total_price = 0
        for orderitem in self.order_products.all():
            total_price += orderitem.product.price * orderitem.count 
        return total_price
    
    # get the product total disount amount
    def get_products_total_discount_price(self):
        total_price = 0
        for orderitem in self.order_products.all():
            if orderitem.product.discount_price is not None:
                total_price += orderitem.product.discount_amount * orderitem.count 
        return total_price
    
    # get the product total price 
    def get_total_price(self):
        total_price = 0
        for orderitem in self.order_products.all():
            if orderitem.product.discount_price is not None:
                total_price += orderitem.product.discount_price * orderitem.count 
            else:
                total_price += orderitem.product.price * orderitem.count 
        return total_price
                
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey('product_module.Product', on_delete=models.CASCADE, verbose_name='محصول')
    color = models.CharField(null=True,blank=True,max_length=20,verbose_name='رنگ محصول')
    count = models.PositiveIntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f'{self.product} - {self.order}'
    
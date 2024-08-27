from django.db import models
import json
# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from account_module.models import User
from webp_imagefield import WebPImageField


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    image = WebPImageField(upload_to= 'images/categories',null=True,blank=True,verbose_name="تصویر دسته بندی")
    icon_name = models.CharField(max_length=20,null=False,blank=False,verbose_name='نام آیکون')
    is_active = models.BooleanField(db_index=True,verbose_name='فعال / غیرفعال')

    def __str__(self):
        return f'( {self.title} - {self.url_title} )'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
        
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    category = models.ManyToManyField(
        ProductCategory, 
        related_name='brands_categories',
        verbose_name='دسته بندی ها'
    )
    image = WebPImageField(upload_to= 'images/categories',null=True,blank=True,verbose_name="تصویر دسته بندی")
    is_active = models.BooleanField(db_index=True,verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title

class ProductTag(models.Model):
    parent = models.ForeignKey('ProductTag',related_name='parent_tag',null=True,blank=True,on_delete=models.CASCADE,verbose_name='تگ والد')
    is_parent = models.BooleanField(verbose_name='والد است')
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.CASCADE       ,     
        related_name='tag_categories',
        verbose_name='دسته بندی ها',
        null=True,blank=True
        ) 
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(db_index=True,verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'
        
    def __str__(self):
        return self.caption

class Product(models.Model):
    title = models.CharField(db_index=True,max_length=300, verbose_name='نام محصول')
    
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.CASCADE       ,     
        related_name='product_categories',
        verbose_name='دسته بندی ها'
    )

    brand = models.ForeignKey(
        'ProductBrand', on_delete=models.CASCADE,
        verbose_name='برند'
    )

    tags = models.ManyToManyField(
        ProductTag,
        related_name='products_tag',
        verbose_name='تگ ها',)

    features = models.TextField(null=True, blank=True, verbose_name='ویژگی ها محصول')
    image = WebPImageField(upload_to='images/products',null=True,blank=True,verbose_name="عکس محصول")
    price = models.IntegerField(db_index=True,verbose_name='قیمت')
    discount_percent = models.IntegerField(default=0,blank=True,null=True, verbose_name='درصد تخفیف')
    discount_expiry = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انقضا تخفیف')
    sales_count = models.IntegerField(db_index=True,editable=False,default=0,verbose_name='مقدار فروخته شده')  # For best-seller
    view_count = models.IntegerField(db_index=True,editable=False,default=0,verbose_name='میزان بازدید')  # For hottest
    short_description = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField( blank=True,null=True,verbose_name='توضیحات اصلی')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False,db_index=True, verbose_name='فعال / غیرفعال')

    colors = models.TextField(blank=True, null=True,verbose_name='رنگ های محصول')
    rate = models.FloatField(default=0.0,verbose_name="میانگین نمرات محصول")
    satisfaction = models.FloatField(default=0.0,verbose_name="درصد رضایت مشتری از محصول")
       
    @property
    def discount_price(self):
        """Calculate and return the discounted price if the discount is still valid."""
        if self.discount_expiry and timezone.now() <= self.discount_expiry:
            discount = (self.discount_percent / 100) * self.price
            return int(max(self.price - discount, 0))
        return None # No discount applied if expired
    
    @property
    def discount_amount(self):
        """Calculate and return the discount amount if the discount is still valid."""
        if self.discount_expiry and timezone.now() <= self.discount_expiry:
            return  self.price - self.discount_price 
        return 0  # Return 0 if no discount is applied or if expired
    
    def get_colors(self):
        """Return the colors as a list."""
        if self.colors:
            return [color.strip() for color in self.colors.split(',')]
        return []

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])
    
    def set_features(self, features_dict):
        self.features = json.dumps(features_dict, ensure_ascii=False)  # Store as JSON without escaping non-ASCII

    def get_features(self):
        if self.features:
            return json.loads(self.features)
        return {}

    def save(self, *args, **kwargs):
        # Handle the 'features' field
        if isinstance(self.features, dict):
            self.features = json.dumps(self.features, ensure_ascii=False, indent=4)  # Ensure non-ASCII characters are not escaped
        elif isinstance(self.features, str):
            try:
                json.loads(self.features)  # Validate JSON
            except (ValueError, TypeError):
                raise ValueError("Invalid JSON string passed to features field")
        else:
            raise ValueError("Features must be a dictionary or a valid JSON string")

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
        
    def get_satisfaction_percentage(self):
        # Total number of comments for this product
        total_comments = self.productcomment_set.count()

        # Number of satisfied comments (e.g., those with a rating of 4 or 5)
        satisfied_comments = self.productcomment_set.filter(rate__gte=4).count()

        if total_comments == 0:
            return 0  # Avoid division by zero

        # Calculate satisfaction percentage
        satisfaction_percentage = (satisfied_comments / total_comments) * 100

        return satisfaction_percentage

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        
        
class ProductGallery(models.Model):
    product = models.ForeignKey(Product,related_name='product_images',on_delete=models.CASCADE,verbose_name='محصول')
    image = WebPImageField(upload_to='images/product-gallery',verbose_name="تصویر")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصولات'

class PriceFilter(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    max_price = models.IntegerField(verbose_name='حداکثر قیمت')
    is_active = models.BooleanField(db_index=True,verbose_name='فعال / غیرفعال')
    
    def __str__(self):
        return f"{self.title} (حداکثر {self.max_price} تومن )"

    class Meta:
        verbose_name = 'فیلتر قیمت'
        verbose_name_plural = 'فیلتر های قیمت'
        

    def __str__(self):
        return self.title
    
class ProductQuestionsAnswers(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('ProductQuestionsAnswers',related_name='question_answers', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_date = models.DateTimeField(db_index=True,auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن پرسش و پاسخ')

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'پرسش و پاسخ محصول'
        verbose_name_plural = 'پرسش ها و پاسخ های مقاله'
        
class ProductComment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_date = models.DateTimeField(db_index=True,auto_now_add=True, verbose_name='تاریخ ثبت')
    comment = models.TextField(verbose_name='کامنت')
    rate = models.PositiveIntegerField(db_index=True,verbose_name='امتیاز')
    likes = models.ManyToManyField(User,related_name='comment_likes',blank=True,verbose_name='لایک')
    dislikes = models.ManyToManyField(User,related_name='comment_dislikes',blank=True,verbose_name='دیس لایک')
    pros = models.CharField(blank=True,max_length=150, null=True,verbose_name='نقات مثبت')
    cons = models.CharField(blank=True,max_length=150, null=True,verbose_name='نقات منفی')
    buyer = models.BooleanField(default=False,verbose_name='خریدار ')

    def __str__(self):
        return str(self.comment)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
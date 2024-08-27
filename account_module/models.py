from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from datetime import datetime, timedelta
from django.utils import timezone
import pyotp
from django.core import validators 
# from utils.custom_fileds import WebPImageField
from webp_imagefield import WebPImageField

class User(AbstractUser):
    profile_picture = WebPImageField(upload_to='images/profile',verbose_name= "تصویر کاربر",null=True,blank=True)
    phone_number = models.CharField(
        null=True,blank=True,
        max_length=11,validators=[validators.MinLengthValidator(11)],
        verbose_name='شماره تلفن کاربر'
        )
    # if it's true gender == man else its woman
    gender = models.BooleanField(null=True, blank=True, verbose_name= 'جنسیت کاربر')
    national_code = models.CharField(
        null=True, blank=True,
        max_length=10, validators=[validators.MinLengthValidator(10)],
        verbose_name='کد ملی کاربر'
        )
    
    postal_code = models.CharField(
        null=True, blank=True,
        max_length=10, validators=[validators.MinLengthValidator(10)],
        verbose_name='کد پستی کاربر'
        )
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    favorite_products = models.ManyToManyField('product_module.Product', related_name='favorite_products',verbose_name='محصولات ذخیره شده')
   
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'


    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        return self.email
    
class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='user')
    code = models.CharField(max_length=6,verbose_name='otp code')
    expiry_time = models.DateTimeField(verbose_name='expiry time')
    
    def __str__(self):
        return self.code

    @staticmethod
    def generate_otp(user):
        try:
            user_otp = OTP.objects.get(user=user)
            if user_otp.expiry_time < timezone.now():
                otp = pyotp.TOTP(pyotp.random_base32(), interval=60)
                otp_code = otp.now()
                expiry_time = timezone.now() + timedelta(minutes=1)
                user_otp.code = otp_code
                user_otp.expiry_time = expiry_time
                user_otp.save() 
            else:
                pass
        except OTP.DoesNotExist:
            otp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            otp_code = otp.now()
            expiry_time = timezone.now() + timedelta(minutes=1)
            user_otp = OTP.objects.create(code=otp_code, expiry_time=expiry_time, user=user)
            user_otp.save()
            
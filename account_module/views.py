from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout
from django.http import HttpRequest,JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .models import User,OTP 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone


class RegisterView(View):
    def get(self,request:HttpRequest):
        context = {
            
        }
        return render(request,'account_module/register.html',context)
    
    def post(self,request:HttpRequest):
        # print(input_type)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        try:
            validate_email(username)
            username_type = True
        except ValidationError:
            username_type = False
            
            

        if username_type:
            user_exsists = User.objects.filter(email__exact=username).exists()
        else:
            user_exsists = User.objects.filter(phone_number=username).exists()
        # if exsists we tell the user 
        if user_exsists:
            context = {'error': 'حسابی با این مشخصات وجود دارد '}
            return render(request,'account_module/register.html',context)
        else:
            # if not creat a new user
            if username_type == True:
                new_user = User(
                    email=username,
                    is_active=True,
                    username = username,   
                )
            else: 
                new_user = User(
                    phone_number=username,
                    is_active=True,
                    username = username,   
                )
                
            new_user.set_password(password)
            new_user.save()
            return redirect(reverse('login-page'))
    

class LoginView(View):
    def get(self,request:HttpRequest):
        context = {
            
        }
        return render(request,'account_module/login.html',context)
    
    def post(self,request:HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        
        try:
            validate_email(username)
            username_type = True
        except ValidationError:
            username_type = False
        
        if username_type:
            user = User.objects.filter(email__exact=username).first()
        else:
            user = User.objects.filter(phone_number=username).first()
        
        if user is not None:
            is_password_correct = user.check_password(password)
            if is_password_correct == True:
                login(request,user)
                return redirect(reverse('home-page'))
            else:
                context = {
                  'error':'رمز عبور اشتباه است.'
                }
                return render(request,'account_module/login.html',context)
        else:
            context = {
                'error':"همچین کاربری وجود ندارد."
            }    
            return render(request,'account_module/login.html',context)


class OTPView(View):
    def get(self,request:HttpRequest):
        username = request.session['username']
        context = {
            
        }
        return render(request,'account_module/sending-code.html',context)
    
    def post(self,request:HttpRequest):
        otp_code = request.POST.get('code')
        username = request.session['username']
        user = None
        
        try:
            validate_email(username)
            username_type = True
        except ValidationError:
            username_type = False
        
        if username_type:
            user = User.objects.filter(email__exact=username).first()
        else:
            user = User.objects.filter(phone_number=username).first()

        db_otp = OTP.objects.filter(user=user).first()
        if otp_code == db_otp.code :
            if db_otp.expiry_time > timezone.now():
                user.is_active =True
                user.save()
                login(request,user)
                return JsonResponse({'message': 'success'})
            else:
                otp = OTP.objects.get(user=user)
                OTP.generate_otp(user=user)
                return JsonResponse({'message': 'error','error':'وقت رمز یکبار مصرف به اتمام رسید.یک کد برای شما پیامک شد لطفا آن را وارد کنید.'})
        else:
            return JsonResponse({'message': 'error','error':'رمز وارد شده اشتباه است.'})

def otp_generate(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username is None:
            username = request.session['username']
        user = None
        
        try:
            validate_email(username)
            username_type = True
        except ValidationError:
            username_type = False  # It's not an email, so treat it as a phone number
        
        if username_type == True:
            user = User.objects.filter(email__exact=username).first()
        else:
            user = User.objects.filter(phone_number=username).first()
        
        if user is not None:
            OTP.generate_otp(user=user)
            otp = OTP.objects.get(user=user)
            request.session['username'] = username
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'error', 'error': 'همچین کاربری وجود ندارد.'})
 
    
def Logout(request):
    logout(request)
    return redirect(reverse('login-page'))
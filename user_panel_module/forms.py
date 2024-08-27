from django import forms
from account_module.models import User
from django.core import validators
from django.core.exceptions import ValidationError

class ProfilePictureModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'id':'uploadProfile',
            })
        }
        
class UserInformationModelForm(forms.ModelForm):
    class Meta:
        model = User
        GENDER_CHOICES = [
        (True, 'آقا'),  # True represents Male
        (False, 'خانم')  # False represents Female
        ]
        fields = ['first_name', 'last_name', 'address', 'national_code', 'gender', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputName',
                'placeholder': "نام خود را وارد کنید..."
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputLName',
                'placeholder': "نام خانوادگی خود را وارد کنید..."
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputStreet',
                'placeholder': "آدرس کامل از استان تا شهر و خیابان و شماره پلاک"
            }),
            'national_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputNationalCode',
                'placeholder': "کد ملی خود را وارد کنید..."
            }),
            'gender': forms.Select(
                choices=GENDER_CHOICES,
                attrs={
                    'class': 'form-select',
                    'id': 'floatingInputGender',
                }
            ),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'floatingInputPhoneNumber',
                'placeholder': "شماره تلفن خود را وارد کنید..."
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name':'نام خانوادگی',
            'address': 'آدرس',
            'national_code':'کد ملی',
            'gender':'جنسیت',
            'phone_number':'شماره تلفن'
        }
        
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="رمز عبور قبلی",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type':"text",
            'id':"floatingInputoldPasswd",
            'placeholder':"رمز عبور قبلی خود را وارد کنید ..."
        }),
        validators=[
            validators.MaxLengthValidator(15),
        ]
    )
    password = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type':"text",
            'id':"floatingInputoldPasswd",
            'placeholder':"رمز عبور جدید خود را وارد کنید ..."
        }),
        validators=[
            validators.MaxLengthValidator(15),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type':"text",
            'id':"floatingInputoldPasswd",
            'placeholder':"رمز عبور جدید خود را دوباره بنویسید ..."
        }),
        validators=[
            validators.MaxLengthValidator(15),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('تکرار رمز عبور جدید با رمز عبور جدید مغایرت دارد')

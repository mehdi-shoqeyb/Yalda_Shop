# from django.http import HttpRequest
# from pyotp import TOTP,random_base32
# from datetime import datetime,timedelta


# def send_otp(request: HttpRequest):
#     totp = TOTP(random_base32(),interval=60)
#     otp = totp.now()
#     request.session['otp_secret_key'] = totp.secret
#     valid_date = datetime.now() + timedelta(minutes=1)
#     request.session['otp_valid_time'] = str(valid_date)

#     print(f'your one time otp {otp}')
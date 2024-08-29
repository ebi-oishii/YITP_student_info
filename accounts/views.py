from django.shortcuts import render
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.views import View
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import MailAuthorizeToken
# Create your views here.

class IndexView(TemplateView):
    template_name = 'accounts/index.html'



class CreateAuthorizeTokenView(View):
    def get(self, request, *args, **kwargs):
        """GETリクエストの際に認証トークンを発行"""
        user = self.request.user
        if not user.mail_auth:
            mail_auth_token = MailAuthorizeToken.objects.create(user=user, expired_at = datetime.now() + timedelta(days=settings.MAIL_AUTH_EXP_DAYS))
            subject = "Please Authorize Your Email Address"
            message = f"URLにアクセスしてメールアドレス認証を完了してください\nhttp://127.0.0.1:8000/users/{mail_auth_token.authorize_token}/activation/"
            from_email = settings.EMAIL_ADDRESS
            recipient_list = [user.email]
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
        else:
            return TemplateResponse(request, 'accounts/index.html')
        
class AuthorizeView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        token = self.kwargs["authorize_token"]
        authorized_user = MailAuthorizeToken.objects.get_user_by_token(token)
        if user != authorized_user:
            return TemplateResponse(request, 'accounts/index.html')
        MailAuthorizeToken.objects.authorize_user_by_token(token)
        if hasattr(authorized_user, 'mail_auth'):
            if authorized_user.mail_auth:
                message = "メール認証が完了しました"
            else:
                message = "メール認証が失敗しています"
        else:
            message = "ユーザーモデルエラーが発生しています"
        return HttpResponse(message)
            
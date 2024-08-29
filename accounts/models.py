from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from datetime import datetime, timedelta
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_mail_auth(self, username, email, password, **extra_fields):
        extra_fields.setdefault('mail_auth', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)
    
    def create_YITP_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_YITP', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)

    def create_staff(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username=username, email=email, password=password, **extra_fields)
    

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""
    class Meta:
        db_table = "custom_user"
    
    is_YITP = models.BooleanField(verbose_name="基研構成員", default=False)
    mail_auth = models.BooleanField(verbose_name="メール認証済み", default=False)
    grade = models.IntegerField(verbose_name="学年", null=True, blank=True)
    grade_note = models.TextField(verbose_name="その他の学年", null=True, blank=True)
    user_id = models.UUIDField(verbose_name="ユーザーID", default=uuid.uuid4, primary=True, editable=False)
    profile_image = models.ImageField(verbose_name="プロフィール写真", null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.user_id
    

class MailAuthorizeTokenManager(models.Manager):
    def authorize_mail_by_token(self, authorize_token):
        authorize_token_valid = self.filter(authorize_token=authorize_token, expired_at__gte=datetime.now()).first()
        if authorize_token_valid:
            user = authorize_token_valid.user
            user.mail_auth = True
            user.save()
            return user
        else:
            raise self.model.DoesNotExist
        
    def get_user_by_token(self, authorize_token):
        user = self.filter(authorize_token=authorize_token).first()
        return user


class MailAuthorizeToken(models.Model):
    """メール認証トークン"""
    class Meta:
        db_table = "mail_authorize_token"
    
    token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="認証トークン")
    authorize_token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = MailAuthorizeTokenManager()

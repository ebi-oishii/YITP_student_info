from django.urls import re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^signup/$', views.SignupView.as_view(), name='signup'),
    re_path(r'^login/$', views.LoginView.as_view(), name="login"),
    re_path(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    re_path(r'^authorize/$', views.CreateAuthorizeTokenView.as_view(), name="create_authorize_token"),
    re_path(r'^(?P<authorize_token>[0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})/$', views.AuthorizeView.as_view(), name='authorize'),
]
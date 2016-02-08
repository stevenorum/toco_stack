"""toco_stack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from toco_stack import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^reset_password$', views.reset_password_view, name='reset_password'),
    url(r'^request_password_reset$', views.request_password_reset_view, name='request_password_reset'),
    url(r'^password_reset_request/(?P<request_id>[0-9a-f]{64})$', views.password_reset_request_view, name='password_reset_request'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^logout_everywhere$', views.logout_everywhere_view, name='logout_everywhere'),
    url(r'^register$', views.register_view, name='register'),
#     url(r'^admin/', admin.site.urls),
]

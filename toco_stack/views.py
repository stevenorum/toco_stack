from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext, loader
import logging
from toco.django.view_helpers import *

logger = logging.getLogger(__name__)

def index_view(request, message=None):
    message = message if message else str(request.COOKIES)
    sessions = []
    if request.user:
        sessions = request.user.active_session_tokens()
    response = render(request, 'index.html', {'message': message, 'sessions':sessions, 'user':request.user, 'session':request.session})
    return response

def password_reset_request_view(request, request_id = None):
    response = render(request, 'index.html', {'reset_code':request_id})
    return response

def request_password_reset_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    email = request.POST.get('email')
    reset_link = '/'.join(request.build_absolute_uri().split('/')[:-1])+'/password_reset_request/'+str(get_reset_code(email))
    send_mail('toco subject', 'Go to {} to reset your password.'.format(reset_link), settings.DEFAULT_FROM_EMAIL,
              [email], fail_silently=False)
    return response

def reset_password_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    if not new_password == confirm_password:
        raise RuntimeError("Password and confirm password must match.")
    reset_code = request.POST.get('reset_code')
    if reset_code:
        reset_password_from_code(new_password, reset_code)
    else:
        reset_password(new_password, request.user, request.POST.get('current_password'))
    return response

def login_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    user, session, cookie_args = login_from_request(request)
    if user:
        response.set_cookie(**cookie_args)
    return response

def logout_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    logout(session=request.session)
    return response

def logout_everywhere_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    logout_everywhere(user=request.user)
    return response

def register_view(request):
    response = HttpResponseRedirect(request.POST.get('redirect_to', '/'))
    user, session, cookie_args = register_from_request(request)
    if user:
        response.set_cookie(**cookie_args)
    return response

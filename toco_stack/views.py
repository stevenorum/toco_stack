from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext, loader
import logging
from toco.user import *

logger = logging.getLogger(__name__)

def index(request, message=None):
    print("Index method beginning.")
    message = message if message else str(request.COOKIES)
    sessions = []
    print(request.session)
    print(request.user)
    if request.user:
#         message = "User: {} ; Session: {}".format(request.user.email, request.session.id)
        sessions = request.user.active_session_tokens()
    response = render(request, 'index.html', {'message': message, 'sessions':sessions, 'user':request.user, 'session':request.session})
    print("Index method ending.")
    return response

def password_reset_request(request, request_id = None):
    print("password_reset_request method beginning.")
    response = render(request, 'index.html', {'password_reset_request_id':request_id})
    print("password_reset_request method ending.")
    return response

# ADD PAGE TO WHICH CUSTOMERS ARE DIRECTED WHEN FOLLOWING A PASSWORD RESET REQUEST LINK

def request_password_reset(request):
    # FINISH IMPLEMENTING
    print("request_password_reset method beginning.")        
    email = request.POST.get('email')
    reset_request = PasswordResetRequest(email=email)
    reset_request.create()
    reset_link = '/'.join(request.build_absolute_uri().split('/')[:-1])+'/password_reset_request/'+str(reset_request.id)
    print(reset_link)
    # SAFETY CHECK FOR DEVELOPMENT - REMOVE LATER
    valid_email_parts = ['stevenorum','toco']
    if [x for x in valid_email_parts if x in email]:
        print(send_mail('toco subject', 'Go to {} to reset your password.'.format(reset_link), settings.DEFAULT_FROM_EMAIL,
                        [email], fail_silently=False))
    print("request_password_reset method ending.")
    return response

def reset_password(request):
    print("reset password method beginning.")        
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    if request.user:
        if not request.user.password_is_correct(request.POST.get('current_password')):
            # ADD ERROR HERE
            return rsponse
    else:
        user = User.load_from_password_reset_request(request.POST.get('reset_request_id'))
        if not user:
            # ADD ERROR HERE
            return response
        request.user = user
    new_password_1 = request.POST.get('password')
    new_password_2 = request.POST.get('confirm_password')
    if new_password_1 == new_password_2:
        request.user.set_password(new_password_1)
    print("reset password method ending.")
    return response

def login(request):
    print("Login method beginning.")
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    email = request.POST.get('email')
    password = request.POST.get('password')

    response = HttpResponseRedirect(request.POST.get('from', '/'))
    if email and password:
        user = User.load_with_auth(email, password)
        if user:
            token = user.get_new_session_token(HTTP_USER_AGENT=request.META.get("HTTP_USER_AGENT"), REMOTE_ADDR=request.META.get("REMOTE_ADDR"))
            response.set_cookie(SessionToken.CKEY, value=token.id, expires=token.expiry_datetime, secure=None, httponly=True)
            request.user=user
            request.session=token
    print("Login method ending.")
    return response

def logout(request):
    try:
        request.session.expire()
    except AttributeError:
        print('request.session not found.')
        pass
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    response.delete_cookie(SessionToken.CKEY)
    return response

def logout_everywhere(request):
    try:
        request.user.purge_sessions()
    except AttributeError:
        print('request.user not found.')
        pass
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    response.delete_cookie(SessionToken.CKEY)
    return response

def register(request):
    email = request.POST.get('email')
    p1 = request.POST.get('password')
    p2 = request.POST.get('confirm_password')

    response = HttpResponseRedirect(request.POST.get('from', '/'))
    try:
        if email and p1 and p2 and p1 == p2:
            user = User(email=email)
            user.set_password(p1)
            user.create()
            token = user.get_new_session_token(HTTP_USER_AGENT=request.META.get("HTTP_USER_AGENT"), REMOTE_ADDR=request.META.get("REMOTE_ADDR"))
            response.set_cookie(SessionToken.CKEY, value=token.id, expires=token.expiry_datetime, secure=None, httponly=True)
    except:
        pass
    return response

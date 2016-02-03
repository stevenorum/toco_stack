from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from toco.user import User, SessionToken


def index(request, message='You\'re at the Toco index page!'):
    message = "No user logged in."
    if request.user:
        message = "User: {} ; Session: {}".format(request.user.email, request.session.id)
    response = render(request, 'index.html', {'message': message})
    return response

def login(request, message='You\'re at the Toco index page!'):
    print("Login called!")
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    email = request.POST.get('email')
    password = request.POST.get('password')

    response = HttpResponseRedirect(request.POST.get('from', '/'))
    if email and password:
        user = User.load_with_auth(email, password)
        if user:
            token = user.get_new_session_token()
            response.set_cookie(SessionToken.CKEY, value=token.id, expires=token.expiry_datetime(), secure=None, httponly=True)
    return response

def logout(request, message='You\'re at the Toco index page!'):
    print("Logout called!")
    try:
        request.session.expire()
    except AttributeError:
        print('request.session not found.')
        pass
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    response.delete_cookie(SessionToken.CKEY)
    return response

def logout_everywhere(request, message='You\'re at the Toco index page!'):
    print("Logout everywhere called!")
    try:
        request.user.purge_sessions()
    except AttributeError:
        print('request.user not found.')
        pass
    response = HttpResponseRedirect(request.POST.get('from', '/'))
    response.delete_cookie(SessionToken.CKEY)
    return response

def register(request, message='You\'re at the Toco index page!'):
    print("Register called!")

    email = request.POST.get('email')
    p1 = request.POST.get('password')
    p2 = request.POST.get('confirm_password')

    response = HttpResponseRedirect(request.POST.get('from', '/'))
    try:
        if email and p1 and p2 and p1 == p2:
            user = User(email=email)
            user.set_password(p1)
            user.create()
            token = user.get_new_session_token()
            response.set_cookie(SessionToken.CKEY, value=token.id, expires=token.expiry_datetime(), secure=None, httponly=True)
    except:
        pass
    return response

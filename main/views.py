from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.forms import *
from main.models import *
import json
import hashlib
import binascii
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from morris_butler.settings import SECRET_KEY, EMAIL_HOST_USER
from calendars.forms import AddingEventForm
from notes.forms import AddNoteForm
from notes.models import Notes


def index(request):
    if request.method == "GET":
        context = {
            'title': "Index page",
            'header': "Index page header",
        }
        if not request.user.is_authenticated:
            sign_in_form = SignInForm()
            context['sign_in_form'] = sign_in_form
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            return render(request, "main/index.html", context)
        else:
            context['add_event_form'] = AddingEventForm()
            context['add_note_form'] = AddNoteForm()
            context['last_notes'] = get_last_notes(request.user)
            context['last_notes_count'] = len(context['last_notes'])
            return render(request, "main/home.html", context)
    else:
        return HttpResponseRedirect('/')


@login_required
def profile_view(request):
    if request.method == "GET":
        form = ChangeUserDataForm()
        context = {
            'title': "User profile page",
            'header': "User profile header",
            'change_user_data_form': form,
        }
        if request.user.is_authenticated:
            return render(request, "main/profile.html", context)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required
def change_user_data_ajax(request):
    response_data = {}
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            result = "Success"
        else:
            result = 'form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def get_last_notes(user):
    all_notes = Notes.get_notes("date_up", user)
    if all_notes.count() >= 3:
        first_three = all_notes[1:4]
    else:
        first_three = all_notes
    return first_three


def send_mail(mail):
    subject = mail['subject']
    text_content = mail['text_content']
    from_email = mail['from_email']
    to_email = mail['to_email']
    html_content = mail['html_content']
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def sign_up_view(request):
    context = {}
    if request.method == "GET":
        if not request.user.is_authenticated:
            context['title'] = "Sign up page"
            context['header'] = "Sign up page header"
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            return render(request, "main/sign_up.html", context)
        else:
            return HttpResponseRedirect('/')
    else:
        response_data = {}
        if not request.user.is_authenticated:
            form = SignUpForm(request.POST)
            if form.is_valid():
                email = form.data['email'].lower()
                username = form.data['username'].lower()
                name = form.data['name']
                surname = form.data['surname']
                pass1 = form.data['password1']
                pass2 = form.data['password2']
                email_uniq = check_email_uniq(email)
                username_uniq = check_username_uniq(username)
                if email_uniq:
                    if username_uniq:
                        if pass1 == pass2:
                            user = User(email=email, username=username, first_name=name, last_name=surname, is_active=0)
                            user.set_password(pass1)
                            user.save()
                            sign_up_key = create_sign_up_key(user, username, pass1)
                            sign_up_key.save()
                            mail = create_mail(user,
                                               "Go to this link to activate your account: 127.0.0.1:8000/activate/" +
                                               sign_up_key.key,
                                               "<a href='http://127.0.0.1:8000/activate/" + sign_up_key.key +
                                               "'>Go to this link to activate your account</a>")
                            send_mail(mail)
                            result = "success"
                        else:
                            result = "Passwords do not match"
                    else:
                        result = "This username is already taken"
                else:
                    result = "This email is already used"

            else:
                result = "Form not valid"
        else:
            result = "User has already signed in"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_mail(user, text, html):
    mail = dict()
    mail['subject'] = 'Dear ' + user.first_name + ' ' + user.last_name + '!'
    mail['from_email'] = EMAIL_HOST_USER
    mail['to_email'] = user.email
    mail['text_content'] = text
    mail['html_content'] = html
    return mail


def create_sign_up_key(user, username, password):
    prepared_hash_object = hashlib.pbkdf2_hmac(hash_name='sha256',
                                               password=(username + password).encode('utf-8'),
                                               salt=SECRET_KEY.encode('utf-8'),
                                               iterations=100000)
    key = binascii.hexlify(prepared_hash_object)
    key = key.decode('utf-8')
    key += str(user.id)
    expiration_date = datetime.now().date()
    expiration_date += timedelta(days=3)
    sign_up_key = SignUpKey(user=user, key=key, expiration_date=expiration_date)
    return sign_up_key


def activate_key(request, key):
    if request.method == "GET":
        keys = SignUpKey.objects.filter(key=key)
        if keys.count() > 0:
            if keys.first().expiration_date >= datetime.now().date():
                user = keys.first().user
                user.is_active = True
                user.save()
                keys.first().delete()
                logout(request)
                login(request, user)
    return HttpResponseRedirect('/')


def check_email_uniq(email):
    return User.objects.filter(email=email).count() == 0


def check_username_uniq(username):
    return User.objects.filter(username=username).count() == 0


def sign_in_ajax(request):
    response_data = {}
    if request.method == "POST":
        if not request.user.is_authenticated:
            form = SignInForm(request.POST)
            if form.is_valid():
                name = form.data['username'].lower()
                password = form.data['password']
                found_user = (len(User.objects.filter(username=name)) > 0) or \
                             (len(User.objects.filter(email=name)) > 0)
                if not found_user:
                    result = "User not found"
                else:
                    user = User.objects.filter(email=name).first()
                    if user is None:
                        user = User.objects.filter(username=name).first()
                    if user.is_active:
                        loginned_user = authenticate(request, username=user.username, password=password)
                        if loginned_user is None:
                            result = "Wrong password"
                        else:
                            login(request, loginned_user)
                            result = "success"
                    else:
                        result = "User was not activated with email"
            else:
                result = "Form not valid"
        else:
            result = "User has already signed in"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def confirm_mail(request, key):
    if len(ConfirmMailKey.objects.filter(request.user).first()) > 0:
        confirm_key = ConfirmMailKey.objects.filter(request.user).first()
        user = request.user
        user.email = confirm_key.email
        confirm_key.delete()
    return HttpResponseRedirect('/')


def create_confirm_email_up_key(user, email):
    prepared_hash_object = hashlib.pbkdf2_hmac(hash_name='sha256',
                                               password=(email).encode('utf-8'),
                                               salt=SECRET_KEY.encode('utf-8'),
                                               iterations=100000)
    key = binascii.hexlify(prepared_hash_object)
    key = key.decode('utf-8')
    key += str(user.id)
    confirm_email_key = ConfirmMailKey(user=user, key=key, email=email)
    return confirm_email_key


def sign_out_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')

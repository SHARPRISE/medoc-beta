from django.http import Http404
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from med_accounts.forms import RegisterForm, LoginForm, UserChangeForm, PatientsModelForm
from med_accounts.models import MyDoctor, Patient

# Create your views here.

def medoc(request):
    """ Afficher tous les medecins de notre database """
    mydoctor = MyDoctor.objects.all()
    """Renders the medoc page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'medoc.html',
        {'mydoctors': mydoctor},
        context_instance = RequestContext(request,
        {
            'title':'Registered Docs',
            'message':"Docs registered with us and ready to serve you!",
            'todocs': "Are you doctor and aren't registed yet? Click on the button below!",
            'year':datetime.now().year,
        })
    )

@login_required
def base(request):
    patient = Patient.objects.all()
    user_on = request.user
    user_short = user_on.get_short_name()
    user_long = user_on.get_full_name()
    user_name = user_on.get_username()
    assert isinstance(request, HttpRequest)
    return render (
        request,
        'base.html',
        {'patients': patient},
        context_instance=RequestContext(request,
        {
            'title': 'Welcome Dr ' + user_long,
            'doctor_name': user_short,
            'message': "Here's the list of your patients sir",
            "user_name": user_name,
            'year': datetime.now().year,
        })
    )


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/medoc/auth_login")


def update_account(request):
    form = UserChangeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)

    return render(request, 'account_home.html', context)


def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if form.is_valid():
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        print (name, password)
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            if next_url is not None:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect("/medoc/base")
    action_url = reverse("auth_login")
    title = "Login"
    submit_btn = title
    submit_btn_class = "btn-success btn-block"
    context = {
        "form": form,
        "action_url": action_url,
        "title": 'Log in',
        "submit_btn": submit_btn,
        "submit_btn_class": submit_btn_class,
        }
    return render(request, "account_login.html", context)


def auth_register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        owner_first_name = form.cleaned_data['owner_first_name']
        owner_last_name = form.cleaned_data['owner_last_name']
        country = form.cleaned_data['country']
        specialite = form.cleaned_data['specialite']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        #MyUser.objects.create_user(name=name, email=email, password=password, country=country, specialite=specialite)
        new_user = MyDoctor()
        new_user.name = name
        new_user.owner_first_name = owner_first_name
        new_user.owner_last_name = owner_last_name
        new_user.email = email
        new_user.country = country
        new_user.specialite = specialite
        #new_user.password = password #WRONG
        new_user.set_password(password) #RIGHT
        new_user.save()
        messages.success(request, "Bienvenue %s" % request.user)

    action_url = reverse("register")
    title = "Register"
    submit_btn = "Create free account"

    context = {
        "form": form,
        "action_url": action_url,
        "title": 'Register now!',
        "submit_btn": submit_btn,
        }
    return render(request, "account_register.html", context)


@login_required
def create_view(request):
    form = PatientsModelForm(request.POST or None)
    user_on = request.user
    user_name = user_on.get_username()
    id =user_on.id
    if form.is_valid():
        patient = form.save(commit=False)
        patient.created_by = user_name
        patient.user_id = id
        patient.save()
    template = "create_view.html"
    context = {
        "form": form,
        "user_name": user_name,
    }
    return render(request, template, context)


@login_required
def update_view(request, object_id=None):
    patient = get_object_or_404(Patient, id=object_id)
    form = PatientsModelForm(request.POST or None, instance=patient)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    template = "account_home.html"
    context = {
        "object": patient,
        "form": form,
    }
    return render(request, template, context)
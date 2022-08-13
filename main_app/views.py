from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from .models import User, Profile
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from rest_framework.reverse import reverse_lazy
from django.views.generic.list import ListView
from .utils import Calendar
from .models import Schedule, Blogpost
from .decorators import user_is_collector, user_is_giver
from django.forms import EmailField


def activation_sent_view(request):
    return render(request, 'activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.signup_confirmation = True
        user.save()
        messages.success(request, 'Your account has been activated')
        if user.is_giver:
            return redirect('main_app:login-user')
        if user.is_collector:
            return redirect('main_app:login_agency')
    else:
        return render(request, 'activation_invalid.html')


def signup_user(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = UserSignUpForm
    return render(request, 'usersignup.html', {'signup_user_form': form})


def signup_agency(request):
    if request.method == 'POST':
        form = AgencySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = AgencySignUpForm
    return render(request, 'companysignup.html', {'signup_agency_form': form})


def login_request(request):
    current_user = request.user
    # if current_user.is_authenticated:
    #     return redirect('main_app:home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_giver:
                    login(request, user)
                    messages.info(request, f'You are now logged in as {username}')
                    return redirect('main_app:home')
                else:
                    messages.error(request, "Your account is a collector's account, Sign in on the collectors page")
                    return redirect('main_app:index')
            else:
                messages.error(request, 'Invalid username or password')

        else:
            messages.error(request, 'Account has not been activated or details have not been entered correctly.')
    form = UserLoginForm
    return render(request=request, template_name='usersignin.html', context={'login_form': form, 'user': current_user})


def login_agency(request):
    current_user = request.user
    # if current_user.is_authenticated:
    #     return redirect('main_app:home')
    if request.method == 'POST':
        form = AgencyLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_collector:
                    login(request, user)
                    messages.info(request, f'You are now logged in as {username}')
                    return redirect('main_app:collect')
                else:
                    messages.error(request, "Your account is a donor's account, Sign in on the donors page")
                    return redirect('main_app:index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Account has not been activated or details have not been entered correctly.')
    form = UserLoginForm
    return render(request=request, template_name='companysignin.html', context={'login_form': form, 'user':current_user})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main_app:index")

@login_required
def home(request):
    user = User.objects.get(id=request.user.id)

    return render(request, 'home.html', {'user': user})


def landing(request):
    user = User.objects.get(id=request.user.id)

    return render(request, 'baseauth.html', {'user':user})


def sign_up_as(request):
    user = User.objects.get(id=request.user.id)
    if user.is_authenticated:
        return redirect('main_app:home')
    return render(request, 'signinas.html')


def index(request):
    user = request.user
    return render(request, 'index.html', {'user':user})

@user_is_giver
@login_required
def my_profile(request):
    p = request.user.profile
    user = p.user
    return render(request, 'my_profile.html', {'profile':p, 'user':user})

@user_is_giver
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('main_app:my_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context ={
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'edit_profile.html', context)


class CalendarView(ListView):
    model = Schedule
    template_name = 'calendar.html'
    success_url = reverse_lazy("calendar")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     date = get_date(self.request.GET.get('month', None))
    #     cal = Calendar(date.year, date.month)
    #     html_cal = calendar.formatmonth(withyear=True)
    #     context['calendar'] = mark_safe(html_cal)
    #     context[prev_month] = prev_month(date)
    #     context[next_month] = next_month(date)
    #
    #     return context


class BlogListView(ListView):
    model = Blogpost
    template_name = 'blog-post2.html'


def post_detail(request, pk):
    post = get_object_or_404(Blogpost, pk =pk)
    user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.author = user
            data.save()
            return redirect('main_app:post_detail', pk = pk)
    else:
        form = NewCommentForm
    return render(request, 'blogpost1.html', {'post': post, 'comment_form':form})


def about(request):
    return render(request, 'About.html')


@user_is_giver
@login_required
def recycle_pickup(request):
    if request.method == 'POST':
        form = NewRequestFormDonor(request.POST)
        if form.is_valid():
            waste = form.cleaned_data.get('waste_type')
            form.waste_type = waste
            form.save()
            messages.success(request, 'Your request has been received, you will be contacted shortly')
            return redirect('main_app:recycle-pickup')

    else:
        form = NewRequestFormDonor
    return render(request, 'recyclable-pickup.html', {'request_form': form})


@user_is_collector
@login_required
def recycle_delivery_agency(request):
    if request.method == 'POST':
        form = NewRequestFormCollector(request.POST)
        if form.is_valid():
            waste = form.cleaned_data.get('waste_type')
            form.waste_type = waste
            form.save()
            messages.success(request, 'Your request has been received, you will be contacted shortly')
            return redirect('main_app:recycle-delivery')

    else:
        form = NewRequestFormCollector
    return render(request, 'recyclable-delivery-agency.html', {'request_form': form})


@user_is_giver
@login_required
def recycle_drop_off(request):
    return render(request, 'recyclable-dropoff.html')


@user_is_collector
@login_required
def recycle_location_agency(request):
    return render(request, 'recyclable-location-agency.html')


@login_required
@user_is_collector
def collect(request):
    return render(request, 'collect.html')

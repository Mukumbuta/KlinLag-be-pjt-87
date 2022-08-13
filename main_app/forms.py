from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from klin_api.models import User
from .models import Profile, Comment, PickupRequest, Waste
from django.forms import EmailField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit






class UserSignUpForm(UserCreationForm):
    confirmation = forms.BooleanField(required=True, error_messages={'required': 'You must agree to our terms'})
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2', 'confirmation')
        help_texts = {

            'password1': None,
            'password2': None,
            'first_name': None,
            'last_name': None,
            'phone': None,
            'email': None,

        }
        widgets = {

            'password1': forms.TextInput(attrs={'placeholder': 'Enter Password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),


        }

    def clean_email(self):
        user_input = self.cleaned_data['email']
        return user_input.lower()


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_giver = True
        if commit:
            user.save()
        return user


class AgencySignUpForm(UserCreationForm):
    confirmation = forms.BooleanField(required=True, error_messages={'required': 'You must agree to our terms'})
    class Meta:
        model = User
        fields = ('first_name', 'phone', 'email', 'password1', 'password2', 'confirmation')
        help_texts = {
            'password1': None,
            'password2': None,
            'first_name': None,
            'phone': None,
            'email': None,
        }
        widgets = {
            'password1': forms.TextInput(attrs={'placeholder': 'Enter Password'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Confirm Password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        user_input = self.cleaned_data['email']
        return user_input.lower()


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_collector = True
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        user_input = self.cleaned_data['username']
        return user_input.lower()


class AgencyLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        user_input = self.cleaned_data['username']
        return user_input.lower()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'location']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']


class NewRequestFormDonor(forms.ModelForm):

    waste_type = forms.ModelMultipleChoiceField(
        queryset=Waste.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = PickupRequest
        fields = ['full_name', 'email', 'phone', 'waste_type', 'address', 'time', 'quantity', 'date', 'extra_note']

    def save(self, commit=True):
        isg = super().save(commit=False)
        isg.is_donor = True
        if commit:
            isg.save()
        return isg


class NewRequestFormCollector(forms.ModelForm):
    waste_type = forms.ModelMultipleChoiceField(
        queryset=Waste.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = PickupRequest
        fields = ['full_name', 'email', 'phone', 'waste_type', 'address', 'time', 'quantity', 'date', 'extra_note']

    def save(self, commit=True):
        isg = super().save(commit=False)
        isg.is_donor = True
        if commit:
            isg.save()
        return isg
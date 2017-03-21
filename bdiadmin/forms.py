from django import forms
from bdiadmin.models import *
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib import messages


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ('name', 'code')


class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ('province', 'name', 'code')


class CollineForm(forms.ModelForm):
    class Meta:
        model = Colline
        fields = ('commune', 'name', 'code')


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = ProfileUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'level', 'telephone',)

    def send_email(self, request):
        try:
            reset_form = PasswordResetForm({'email': self.cleaned_data['email']})
            assert reset_form.is_valid()
            reset_form.save(
                request=request,
                from_email="cmam.burundi@gmail.com",
                use_https=request.is_secure(),
                subject_template_name='bdiadmin/account_creation_subject.txt',
                email_template_name='bdiadmin/account_creation_email.html',
            )
            messages.success(request, _('Profile created and mail sent to {0}.').format(self.cleaned_data['email']))
        except:
            messages.warning(request, _('Profil created, but unable to send mail to {0}.').format(self.cleaned_data['email']))
            pass


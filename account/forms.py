from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'profile_image', 'education_status', 'phone_number', 'job_title', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'profile_image', 'education_status', 'phone_number', 'job_title')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Exception as e:
            print(e)
            return email
        raise forms.ValidationError('Email "%s" is already in use' % email)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except:
            return username
        raise forms.ValidationError('Username "%s" is already in use' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.profile_image = self.cleaned_data['profile_image']
        if commit:
            account.save()
        return account

class AccountDeleteForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ()








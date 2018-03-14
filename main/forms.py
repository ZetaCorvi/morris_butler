from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(label='Email or username', max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter your e-mail or username'}))
    password = forms.CharField(label='Password', max_length=200,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter your password'}))


class SignUpForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=200,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Enter your e-mail'}))
    username = forms.CharField(label='Username', max_length=200,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter your username'}))
    name = forms.CharField(label='Name', max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter your name'}))
    surname = forms.CharField(label='Surname', max_length=200,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Enter your surname'}))
    password1 = forms.CharField(label='Password', max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Password again', max_length=200,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Enter your password again'}))


class ChangeUserDataForm(forms.Form):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter new e-mail'}))
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                             'placeholder': 'Enter new username'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter new name'}))
    surname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Enter new surname'}))
    old_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                     'placeholder': 'Enter osd password'}))
    password1 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Enter new password'}))
    password2 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Enter new password again'}))

from django import forms


class LoginForm(forms.Form):
	login = forms.CharField(label='login', max_length=100)
	password = forms. CharField(label='hasło', widget=forms.PasswordInput())


class RegisterForm(forms.Form):
	login = forms.CharField(label='login', max_length=100)
	email = forms.EmailField(label='email', max_length=100)
	password = forms.CharField(label='hasło', widget=forms.PasswordInput())
	password2 = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput())
	first_name = forms.CharField(label='Imię', max_length=100, required=False)
	last_name = forms.CharField(label='Nazwisko', max_length=100, required=False)
	motto = forms.CharField(label='Powiedzonko', widget=forms.Textarea, max_length=140, required=False)


class EditForm(forms.Form):
	login = forms.CharField(label='login', max_length=100)
	email = forms.EmailField(label='email', max_length=100)
	first_name = forms.CharField(label='Imię', max_length=100, required=False)
	last_name = forms.CharField(label='Nazwisko', max_length=100, required=False)
	motto = forms.CharField(label='Powiedzonko', widget=forms.Textarea, max_length=140,required=False)


class EditPasswordForm(forms.Form):
	password0 = forms.CharField(label='stare hasło', widget=forms.PasswordInput())
	password1 = forms.CharField(label='nowe hasło', widget=forms.PasswordInput())
	password2 = forms.CharField(label='powtórz hasło', widget=forms.PasswordInput())

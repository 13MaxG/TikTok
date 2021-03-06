from django import forms


class CommentForm(forms.Form):
	content = forms.CharField(label='Treść', widget=forms.Textarea)

	
class GetPrivilegeForm(forms.Form):
	hash = forms.CharField(label='Kod dostępu', widget=forms.Textarea)


class SendPrivilegesForm(forms.Form):
	emails = forms.CharField(label='Emaile(każdy w nowej linii)', widget=forms.Textarea)
	
	
class SubmitForm(forms.Form):
	code = forms.CharField(label='Kod', widget=forms.Textarea)


class CreateForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=100)
	pdf_file = forms.FileField(label='Plik PDF',)


class CreateGroupForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=100)
	shortname = forms.CharField(label='Skrót', max_length=100)
	open = forms.BooleanField (label='Dostęp otwarty', initial=True, required=False)


class TestProgramForm(forms.Form):
	code = forms.CharField(label='Kod testu', widget=forms.Textarea)
	time = forms.FloatField(label='Maksymalny czas wykonywania', initial=10.0)


class DeletionForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=100)


class EditNameForm(forms.Form):
	name = forms.CharField(label='Nazwa', max_length=100)


class EditPDFForm(forms.Form):
	pdf_file = forms.FileField(label='Plik PDF')

from django import forms


class NewsForm(forms.Form):
    content = forms.CharField(label='Treść', widget=forms.Textarea)


from django import forms
class FindWordForm(forms.Form):
    word = forms.CharField(max_length=100)
     
from django import forms

class JobForm(forms.Form):
	input_text = forms.CharField(label='Hashtag', max_length=50)

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django_email_verification import send_email

class RegisterForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ('name', 'email', 'contact', 'college_id_number', 'college', 'department', 'course', 'year',)

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		if commit:
			user.is_active = False
			send_email(user)
			user.save()
		return user

class UpdateForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ('name', 'contact', 'college_id_number', 'college', 'department', 'course', 'year', 'events')
		widgets = {'events' : forms.CheckboxSelectMultiple()}

class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('team_name', 'event', 'user',)
		widgets = {'user': forms.HiddenInput()}
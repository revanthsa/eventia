from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView

class EventDetailView(DetailView):
    model = Event
    template_name = 'dashboard/events.html'

class Register(SuccessMessageMixin, CreateView):
	success_url = reverse_lazy('login')
	success_message = _('Account has been sucessfully created! Check your mail and verify your account before signing in.')
	form_class = RegisterForm
	template_name = 'register.html'

@login_required
def Profile(request):
	if request.user.is_superuser:
		return redirect('/admin/core/user/')
	if request.method == 'POST':
		form = UpdateForm(data=request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, _('Your profile has been updated!'))
			return redirect(reverse_lazy('profile'))
	else:
		form = UpdateForm(instance=request.user)

	if request.user.is_staff:
		msg = Message.objects.filter(for_staff=True).order_by('-id')
	else:
		msg = Message.objects.filter(for_staff=False).order_by('-id')
	context = {
		'form': form,
		'msg' : msg,
	}
	return render(request, 'dashboard/profile.html', context)

@login_required
def TeamView(request):
	if request.user.is_superuser or request.user.is_staff:
		return redirect(reverse_lazy('admin:login'))
	if request.method == 'POST':
		form = TeamForm(data=request.POST)
		try:
			join_team_check = Team.objects.get(team_name=form.data['team_name'], event=form.data['event'])
		except:
			join_team_check = None
		if join_team_check:
			join_team_check.user.add(request.user)
			messages.success(request, _('Your team has been updated!'))
			return redirect(reverse_lazy('teams'))
		else:
			if form.is_valid():
				form.save()
				form.instance.user.add(request.user)
				messages.success(request, _('You have successfully created a team!'))
				return redirect(reverse_lazy('teams'))
			return redirect(reverse_lazy('teams'))
	else:
		form = TeamForm()
		form.fields['event'].queryset = request.user.events.all()
		
		# find user list of teams joined by user for registed events
		user_registered_events = [i.id for i in request.user.events.all()]
		team_user_registered_events = [i.event.id for i in Team.objects.filter(event_id__in=user_registered_events, user=request.user)]
		no_team_user_registered_events = list(list(set(user_registered_events)-set(team_user_registered_events)) + list(set(team_user_registered_events)-set(user_registered_events)))
		if no_team_user_registered_events != []:
			form.fields['event'].queryset = Event.objects.filter(id__in=no_team_user_registered_events)

		no_form = False
		# user joined in teams for all registed events
		if no_team_user_registered_events == []:
			no_form = True

	msg = Message.objects.filter(for_staff=False).order_by('-id')
	context = {
		'form': form,
		'msg' : msg,
		'no_form' : no_form,
	}
	return render(request, 'dashboard/teams.html', context)

class Dashboard(LoginRequiredMixin, View):
	login_url = reverse_lazy('login')

	def get(self, request):
		if request.user.is_superuser or request.user.is_staff:
			return redirect(reverse_lazy('admin:login'))
		else:
			winner = {}
			if request.user.team_set.all():
				winner_team_id = []
				for i in request.user.team_set.all():
					winner_team_id.append(i.id)
				winner = Winner.objects.filter(team_id__in=winner_team_id)
			
			msg = Message.objects.filter(for_staff=False).order_by('-id')
			context = {
				'msg' : msg,
				'winner': winner,
			}
			return render(request, 'dashboard/dashboard.html', context)
		return redirect(reverse_lazy('login'))
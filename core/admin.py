from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *

User = get_user_model()

class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		(_('Personal info'), {'fields': ('name', 'contact', 'college_id_number', 'college', 'department', 'course', 'year',)}),
		(_('Events'), {'fields': ('events',)}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
	)

	staff_fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('name', 'contact', 'college_id_number', 'college', 'department', 'course', 'year',)}),
		(_('Events'), {'fields': ('events',)}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups',)}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('name', 'email', 'contact', 'college_id_number', 'college', 'department', 'course', 'year', 'password1', 'password2',),
		}),
	)

	list_display = ('name', 'email', 'contact', 'is_staff',)
	search_fields = ('name', 'contact', 'email', 'college_id_number', 'college', 'department', 'course', 'year',)
	ordering = ('date_joined',)
	list_filter = ('groups', 'is_staff', 'year', 'events',)
	filter_horizontal = UserAdmin.filter_horizontal + ('events',)

	def get_queryset(self, request):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='event_organizer').exists():
				return User.objects.all()
			elif request.user.groups.filter(name='event_manager').exists():
				event_manager_events = []
				for i in request.user.events.all():
					event_manager_events.append(i)
				return User.objects.filter(events__in=event_manager_events)
		return User.objects.all()

	def get_fieldsets(self, request, obj=None):
		if not request.user.is_superuser:
			return self.staff_fieldsets
		return super(CustomUserAdmin, self).get_fieldsets(request, obj)

class MessageAdmin(admin.ModelAdmin):
	list_display = ('message', 'for_staff', 'created_by', 'created_on',)
	search_fields = ('message', 'created_by__email', 'created_on',)
	list_filter = ('for_staff',)
	readonly_fields = ('created_by', 'created_on',)

	def save_model(self, request, obj, form, change):
		if not obj.created_by:
			obj.created_by = request.user
		obj.save()

class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'levels', 'date', 'location',)
	search_fields = ('name', 'levels', 'date', 'location', 'description', 'tags')
	autocomplete_fields = ('head_user',)
	eventManager_readonly_fields = ('head_user',)
	
	def get_queryset(self, request):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='event_organizer').exists():
				return Event.objects.all()
			elif request.user.groups.filter(name='event_manager').exists():
				return Event.objects.filter(head_user=request.user)
		return Event.objects.all()

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='event_manager').exists():
			return self.eventManager_readonly_fields
		return super(EventAdmin, self).get_readonly_fields(request, obj)

class TeamAdmin(admin.ModelAdmin):
	list_display = ('team_name',)
	search_fields = ('team_name',)
	autocomplete_fields = ('event',)
	filter_horizontal = ('user',)
	eventManager_readonly_fields = ('team_name', 'event', 'user')

	def get_queryset(self, request):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='event_organizer').exists():
				return Team.objects.all()
			elif request.user.groups.filter(name='event_manager').exists():
				event_manager_events = []
				for i in request.user.events.all():
					event_manager_events.append(i.id)
				return Team.objects.filter(event_id__in=event_manager_events)
		return Team.objects.all()

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='event_manager').exists() or request.user.groups.filter(name='event_organizer').exists():
			return self.eventManager_readonly_fields
		return super(TeamAdmin, self).get_readonly_fields(request, obj)

class WinnerAdmin(admin.ModelAdmin):
	list_display = ('team', 'event', 'position')
	search_fields = ('team__team_name', 'event__name', 'position')
	list_filter = ('event__name', 'position',)
	autocomplete_fields = ('team', 'event',)

	def get_queryset(self, request):
		if not request.user.is_superuser:
			if request.user.groups.filter(name='event_organizer').exists():
				return Winner.objects.all()
			elif request.user.groups.filter(name='event_manager').exists():
				event_manager_events = []
				for i in request.user.events.all():
					event_manager_events.append(i.id)
				return Winner.objects.filter(event_id__in=event_manager_events)
		return Winner.objects.all()

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.user.groups.filter(name='event_manager').exists():
			event_manager_events = []
			for i in request.user.events.all():
				event_manager_events.append(i.id)
			if db_field.name == 'event':
				kwargs['queryset'] = Event.objects.filter(id__in=event_manager_events)
			if db_field.name == 'team':
				kwargs['queryset'] = Team.objects.filter(event_id__in=event_manager_events)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.site_title = "Eventia admin login"
admin.site.index_title = "Dashboard"
admin.site.site_header = "Eventia"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Winner, WinnerAdmin)
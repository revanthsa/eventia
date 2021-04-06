from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from datetime import date
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from django.core.mail import send_mail

class Event(models.Model):
	class Meta:
		verbose_name = _('event')
		verbose_name_plural = _('events')

	def date_validator(value):
		if value:
			if value < date.today():
				raise ValidationError(_('Event date cannot be in the past'))
			else:
				return value
		raise ValidationError(_('Event date must be set'))

	name = models.CharField(_('event name'), max_length=30, unique=True)
	description = models.TextField(_('event description'))
	tags = models.TextField(_('event tags'), help_text=_('seperate the tags with a \",\"'))
	levels = models.PositiveIntegerField(_('total levels in the event'), validators=[MaxValueValidator(10)])
	date = models.DateField(_('date of event'), validators=[date_validator])
	time = models.TimeField(_('Starting Time of event'), null=True)
	location = models.CharField(_('location of the event'), max_length=100)
	slogan = models.TextField(_('slogan'), blank=True, null=True)
	quote = models.TextField(_('quote'), blank=True, null=True)
	instructions = models.TextField(_('instructions'), help_text=_('Instructions for the participants'), null=True)
	head_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, limit_choices_to={'is_staff': True})
	slug = models.SlugField(help_text=_('url value field for events'), null=True, unique=True)
	image = models.ImageField(upload_to = 'events/', null=True)

	def get_absolute_url(self):
		return reverse('events', kwargs={'slug': self.slug})

	def __str__(self):
		return str(self.name)

class Team(models.Model):
	class Meta:
		verbose_name = _('team')
		verbose_name_plural = _('teams')
		constraints = [
			models.UniqueConstraint(fields=('team_name', 'event'), name='unique_team_event'),
		]

	team_name = models.CharField(max_length=25, help_text=_('Team name must be unique (case-sensitive)'))
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
	current_level = models.PositiveIntegerField(_('current level'), default=0)

	def __str__(self):
		return str(self.team_name)

	def save(self, **kwargs):
		super().save(*kwargs)
		transaction.on_commit(self.sendMail)

	def sendMail(self):
		if self.id:
			if self.current_level > 0:
				recepient = []
				for user in self.user.all():
					recepient.append(user.email)
				if recepient != []:
					subject = 'Eventia - ' + str(self.event.name)
					message = 'Your team \"'+ str(self.team_name) + '\" has been selected for round ' + str(self.current_level) + ' in ' + str(self.event.name) + '\n\n\n\nRegards,\nTeam Eventia'
					send_mail(subject, message, settings.EMAIL_HOST_USER, recepient, fail_silently = False)
		super().save()

class User_Manager(BaseUserManager):
	def _create_user(self, name, email, college_id_number, college, department, course, year, password=None, **extra_fields):
		if not name:
			raise ValueError(_('Name must be set'))
		if not email:
			raise ValueError(_('Email must be set'))
		if not college_id_number:
			raise ValueError(_('College ID Number must be set'))
		if not college:
			raise ValueError(_('college must be set'))
		if not department:
			raise ValueError(_('Name must be set'))
		if not course:
			raise ValueError(_('course must be set'))
		if not year:
			raise ValueError(_('year must be set'))
		email = self.normalize_email(email)
		user = self.model(name=name, email=email, college_id_number=college_id_number, college=college, department=department, course=course, year=year, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, name, email, college_id_number, college, department, course, year, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', False)
		return self._create_user(name, email, college_id_number, college, department, course, year, password, **extra_fields)

	def create_superuser(self, name, email, college_id_number, college, department, course, year, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self._create_user(name, email, college_id_number, college, department, course, year, password, **extra_fields)

class User(AbstractUser):
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	first_name = None
	last_name = None
	username = None

	YEAR_CHOICES = (
		('1st', '1st'),
		('2nd', '2nd'),
		('3rd', '3rd'),
		('4th', '4th'),
		('5th', '5th'),
	)

	name = models.CharField(_('name'), max_length=30, validators=[MinLengthValidator(3)])
	email = models.EmailField(_('email address'), primary_key=True)
	contact = PhoneNumberField(_('contact number'), max_length=13, null=True, blank=True, unique=True, help_text=_('Contact Number is optional'))
	college_id_number = models.CharField(_('college roll number'), max_length=20, unique=True)
	college = models.CharField(_('college'), max_length=150)
	department = models.CharField(_('department'), max_length=60)
	course = models.CharField(_('course'), max_length=20)
	year = models.CharField(_('year'), choices=YEAR_CHOICES, max_length=3)
	events = models.ManyToManyField(Event, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'college_id_number', 'college', 'department', 'course', 'year']

	objects = User_Manager()

	def __str__(self):
		return str(self.email)

class Message(models.Model):
	class Meta:
		verbose_name = _('message')
		verbose_name_plural = _('messages')

	created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
	message = models.TextField(_('message'))
	created_on = models.DateField(_('created on'), auto_now_add=True)
	for_staff = models.BooleanField(_('message for staff?'), default=False) 

	def __str__(self):
		return str(self.message)

class Winner(models.Model):
	class Meta:
		verbose_name = _('winner')
		verbose_name_plural = _('winners')

	team = models.ForeignKey(Team, on_delete=models.CASCADE, help_text=_('If the winner is a group of participant, choose the team from here'))
	event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text=_('Choose the event in which they won'))
	position = models.CharField(_('winning position'), max_length=10, help_text=_('Enter the winning position of the participant or team'))

	def __str__(self):
		return str(self.team.team_name) + " won " + str(self.position) + " position in " + str(self.event.name)
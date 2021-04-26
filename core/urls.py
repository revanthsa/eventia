from django.urls import path, include, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
	path('', RedirectView.as_view(url=reverse_lazy('login')), name='home'),
	path('events/<slug:slug>/', EventDetailView.as_view(), name='events'),

	path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name="login"),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),

	path('register/', Register.as_view(), name="register"),
	path('dashboard/', Dashboard.as_view(), name="dashboard"),
	path('profile/', Profile, name="profile"),
	path('teams/', TeamView, name="teams"),

	path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done/'), name="password_change"),
	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
	path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done/', html_email_template_name='registration/password_reset_email.html'), name="password_reset"),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/reset/done/', post_reset_login=True), name="password_reset_confirm"),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
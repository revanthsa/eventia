import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['http://eventia1.herokuapp.com', 'https://eventia1.herokuapp.com']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'cloudinary_storage',
	'django.contrib.staticfiles',
	'core',
	'cloudinary',
	'crispy_forms',
	'phonenumber_field',
	'django_email_verification',
	'django_extensions',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventia.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'eventia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
	 'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USER'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'HOST': os.environ.get('DB_HOST'),
		'PORT': '5432',
	 }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Custom User Model
AUTH_USER_MODEL = 'core.User'

LOGIN_REDIRECT_URL='/dashboard/'
LOGIN_URL='/login/'
LOGOUT_REDIRECT_URL='/login/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 5
SESSION_SAVE_EVERY_REQUEST = True

PASSWORD_RESET_TIMEOUT = 300

# Default country from phone field
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'IN'

# Mail Server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
# EMAIL_USE_LOCALTIME = True

def verified_callback(user):
	user.is_active = True

EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_ADDRESS = os.environ.get('EMAIL_HOST_USER')
EMAIL_FROM_ADDRESS = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_MAIL_SUBJECT = 'Confirm your email'
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_PAGE_TEMPLATE = 'confirm_template.html'
EMAIL_MAIL_PLAIN = 'mail_body.txt'
EMAIL_PAGE_DOMAIN = 'https://eventia1.herokuapp.com/'
EMAIL_TOKEN_LIFE = 60 * 5

GRAPH_MODELS = {
	'all_applications':True,
	'group_models':True,
}

# A list of all the people who get code error notifications, when DEBUG=False
ADMINS = [('Revanth', 'revanthlp3@gmail.com'), ('Sree Varshini', 'sreevarshini13@gmail.com')]

import django_heroku
django_heroku.settings(locals())

CLOUDINARY_STORAGE = {
	'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
	'API_KEY': os.environ.get('API_KEY'),
	'API_SECRET': os.environ.get('API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
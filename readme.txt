basic_api is a standalone django-app that can be used directly, but it requires some setup-

1. Install all the requirements in your virtual env-
	pip install -r requirements.txt

2. Make these changes in settings.py-
			INSTALLED_APPS = [
			 	 ...
		    'rest_framework',
		    'corsheaders',
		    'basic_api'
		]

			MIDDLEWARE = [
		    'django.middleware.security.SecurityMiddleware',
		    'django.contrib.sessions.middleware.SessionMiddleware',
		    'corsheaders.middleware.CorsMiddleware',
				...
		]

		ROOT_URLCONF = 'core.urls'

		REST_FRAMEWORK = {
		    'DEFAULT_PERMISSION_CLASSES': [
		        'rest_framework.permissions.AllowAny',
		    ],
		    'DEFAULT_AUTHENTICATION_CLASSES': (
		        'rest_framework_simplejwt.authentication.JWTAuthentication',
		    )
		}

		CORS_ALLOWED_ORIGINS = [
		    "http://127.0.0.1:3000",
		    "http://localhost:3000"
		]

		AUTHENTICATION_BACKENDS = ('core.emailbackend.EmailBackend',)

		SIMPLE_JWT = {
		    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
		    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
		    'ROTATE_REFRESH_TOKENS': True,
		    'BLACKLIST_AFTER_ROTATION': True,
		    'UPDATE_LAST_LOGIN': False,

		    'ALGORITHM': 'HS256',
		    'SIGNING_KEY': SECRET_KEY,
		    'VERIFYING_KEY': None,
		    'AUDIENCE': None,
		    'ISSUER': None,

		    'AUTH_HEADER_TYPES': ('Bearer',),
		    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
		    'USER_ID_FIELD': 'id',
		    'USER_ID_CLAIM': 'user_id',
		    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

		    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
		    'TOKEN_TYPE_CLAIM': 'token_type',

		    'JTI_CLAIM': 'jti',

		    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
		    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
		    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
		}

3. Create a new file, "emailbackend.py" to enable login with email and
	 the following code to the file-

	 from django.contrib.auth.backends import ModelBackend, UserModel
	 from django.db.models import Q

	 class EmailBackend(ModelBackend):
	     def authenticate(self, request, username=None, password=None, **kwargs):
	         try: #to allow authentication through phone number or any other field, modify the below statement
	             user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
	         except UserModel.DoesNotExist:
	             UserModel().set_password(password)
	         except MultipleObjectsReturned:
	             return User.objects.filter(email=username).order_by('id').first()
	         else:
	             if user.check_password(password) and self.user_can_authenticate(user):
	                 return user

	     def get_user(self, user_id):
	         try:
	             user = UserModel.objects.get(pk=user_id)
	         except UserModel.DoesNotExist:
	             return None

	         return user if self.user_can_authenticate(user) else None

from core.env import BASE_DIR, env

ENV_PATH = BASE_DIR / ".env"

env.read_env(ENV_PATH)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-bzo92jqsu8x&a2u=re-thfmf#c@p-^^nfmusqwm!w%ja)b)ctg",  # type: ignore
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

# Application definition

INTERNAL_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "debug_toolbar",
    "drf_standardized_errors",
    "auditlog",
]

CUSTOM_APPS = [
    "apps.authentication",
    "apps.authorization",
    "apps.company",
    "apps.user",
    "apps.address",
    "apps.action",
    "apps.country",
    "apps.division",
    "apps.district",
    "apps.sub_district",
    "apps.data_migration",
    "apps.product",
    "apps.uom",
    "apps.sale_order",
    "apps.menu",
    "apps.blog",
    "apps.offer",
    "apps.social_auth",
]


INSTALLED_APPS = INTERNAL_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middlewares.AuditlogMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "core"]
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "user.User"


# creating app log directory
LOG_DIR = BASE_DIR / "logs"

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)


# Django Session settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

# Django Base CSRF settings
CSRF_COOKIE_AGE = 86400  # 1 day approx.
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_PATH = "/"
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

# DRF UNHANDLED EXCEPTION
DRF_STANDARDIZED_ERRORS = {
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True,
    "EXCEPTION_HANDLER_CLASS": "core.exceptions.handlers.CoreExceptionHandler",
}


# SENTRY
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_ENV = env("SENTRY_ENV")
SENTRY_DEBUG = env.bool("SENTRY_DEBUG", default=False)  # type: ignore

# GOOGLE OAUTH2
GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID", default=None)  # type: ignore

from core.settings.plugins.sentry import *  # noqa: E402, F403, I001
from core.settings.plugins.unfold import *  # noqa: E402, F403, I001
from core.settings.plugins.logging import *  # noqa: E402, F403, I001
from core.settings.plugins.cors import *  # noqa: E402, F403, I001
from core.settings.plugins.drf import *  # noqa: E402, F403, I001
from core.settings.plugins.jwt import *  # noqa: E402, F403, I001
from core.settings.plugins.auditlog import *  # noqa: E402, F403, I001
from core.settings.plugins.drf_spectacular import *  # noqa: E402, F403, I001

import os


DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
ROOT_URLCONF = 'tests.urls'
SITE_ID = 1
LANGUAGE_CODE = 'en'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'OPTIONS': {
        'context_processors': (
            "django.contrib.auth.context_processors.auth",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.request",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.core.context_processors.request",
            "django.contrib.messages.context_processors.messages",
            "sekizai.context_processors.sekizai",
            "cms.context_processors.cms_settings",
        ),
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    },
    'DIRS': (
        os.path.join('tests', 'templates'),
    )
}]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'treebeard',
    'cms',
    'menus',
    'djangocms_text_ckeditor',
    'djangocms_local_navigation',
)

CMS_TEMPLATES = (
    ('base.html', 'Base'),
)

CMS_PLUGIN_PROCESSORS = (
    'djangocms_local_navigation.cms_plugin_processors.add_ids_to_content',
)

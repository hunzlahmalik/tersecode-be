import os

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# using the postgresql database
# fill in the following values for your postgresql database
# using the env file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

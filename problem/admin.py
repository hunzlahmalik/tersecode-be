from django.contrib import admin
from .models import Problem

for model in [Problem]:
    admin.site.register(model)

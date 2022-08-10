from django.contrib import admin
from .models import Problem, Language, Tag, Solution

for model in [Problem, Language, Tag, Solution]:
    admin.site.register(model)

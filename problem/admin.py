from django.contrib import admin
from .models import Problem, Language, Tag, Solution, TestCase

for model in [Problem, Language, Tag, Solution, TestCase]:
    admin.site.register(model)

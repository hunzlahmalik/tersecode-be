from django.contrib import admin
from .models import Problem, Language, Tag, Solution, TestCase, Discussion

for model in [Problem, Language, Tag, Solution, TestCase, Discussion]:
    admin.site.register(model)

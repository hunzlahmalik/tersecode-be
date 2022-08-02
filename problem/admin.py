from django.contrib import admin
from .models import Problem, Language, ProblemTag, Tag, Solution

for model in [Problem, Language, ProblemTag, Tag, Solution]:
    admin.site.register(model)

from django import forms
from django.shortcuts import get_object_or_404
from .models import Solution, Problem
from submission.models import Submission


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['problem', 'language', 'solution']

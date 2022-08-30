from django.contrib import admin

from .models import Submission, SubmissionAnalytics

admin.site.register(Submission)
admin.site.register(SubmissionAnalytics)

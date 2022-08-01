from django.db import models


class Problem(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    difficulty = models.CharField(
        max_length=1,
        choices=[('E', 'Easy'),
                 ('M', 'Medium'),
                 ('H', 'Hard')],
        default='E'
    )
    statement = models.FileField(upload_to='problem/static/problem/')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

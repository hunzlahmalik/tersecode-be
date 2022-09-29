from django.db import models

from users.models import User
from .problem import Problem


class Discussion(models.Model):
    """
    Discussion model.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="discussions", help_text="User"
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="discussions",
        help_text="Problem",
    )
    content = models.TextField(help_text="Discussion content")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Discussion timestamp"
    )

    def __str__(self):
        return (
            self.user.username + " - " + self.problem.title + " - " + self.content[:10]
        )

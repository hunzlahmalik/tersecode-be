from django.db import models


class Language(models.Model):
    """
    Programming language model.
    """

    class Name(models.TextChoices):
        C = "c", "C"
        CPP = "cpp", "C++"
        JAVA = "java", "Java"
        PYTHON = "python", "Python"
        PYTHON3 = "python3", "Python3"
        PYTHON2 = "python2", "Python2"
        JAVASCRIPT = "javascript", "JavaScript"
        GO = "go", "Go"
        HASKELL = "haskell", "Haskell"
        RUBY = "ruby", "Ruby"
        RUST = "rust", "Rust"
        KOTLIN = "kotlin", "Kotlin"
        SWIFT = "swift", "Swift"
        JAVA8 = "java8", "Java8"
        JAVA9 = "java9", "Java9"
        JAVA10 = "java10", "Java10"
        JAVA11 = "java11", "Java11"

    name = models.CharField(
        max_length=50, choices=Name.choices, help_text="Language name"
    )
    extension = models.CharField(
        max_length=10, null=True, blank=True, help_text="Language extension"
    )

    def __str__(self):
        return self.name

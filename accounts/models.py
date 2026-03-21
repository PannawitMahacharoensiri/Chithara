from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

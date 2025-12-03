from django.db import models

class User(models.Model):
    token = models.CharField(max_length=140, default='DEFAULT')
    username = models.CharField(max_length=140, default='DEFAULT')
    email = models.EmailField()
    type = models.CharField()

    def __str__(self):
        return f"{self.username}"

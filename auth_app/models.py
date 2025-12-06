from django.db import models

class UserProfile(models.Model):
    token = models.CharField(max_length=140, default='DEFAULT')
    username = models.CharField(max_length=140)
    email = models.EmailField()
    user_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username}"

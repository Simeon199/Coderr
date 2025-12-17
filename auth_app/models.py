from django.db import models

class UserProfile(models.Model):
    token = models.CharField(max_length=140, default='DEFAULT')
    username = models.CharField(max_length=140)
    email = models.EmailField()
    user_id = models.IntegerField(default=0)
    type = models.CharField(default="customer")
    first_name = models.CharField(blank=True)
    last_name = models.CharField(blank=True)
    file = models.CharField(blank=True)
    location = models.CharField(blank=True)
    tel = models.CharField(blank=True)
    description = models.CharField(blank=True)
    working_hours = models.CharField(blank=True)

    def __str__(self):
        return f"{self.username}"

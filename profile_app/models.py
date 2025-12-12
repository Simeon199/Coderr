from django.db import models

class CustomerProfile(models.Model):
    user = models.IntegerField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    file = models.CharField(max_length=100),
    uploaded_at = models.DateTimeField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.type}"

class BusinessProfile(models.Model):
    user = models.IntegerField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    description = models.TextField()
    working_hours = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} - {self.location}" 
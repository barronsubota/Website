from django.db import models

# Create your models here.
# students/models.py

from django.contrib.auth.models import User
from slugify import slugify


class StudentCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    series = models.CharField(max_length=10)
    issue_date = models.DateField()
    valid_until = models.DateField()
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    form_of_study = models.CharField(max_length=50)
    faculty = models.CharField(max_length=100)
    structural_unit = models.CharField(max_length=100)
    group_number = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Generate a slug from the user's full name
        self.slug = slugify(f'{self.name} {self.surname}')
        super().save(*args, **kwargs)

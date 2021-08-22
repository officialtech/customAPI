from django.db import models

class Student(models.Model):
    roll_no = models.IntegerField()
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=100)
    registration_no = models.IntegerField()


    def __str__(self):
        return self.name
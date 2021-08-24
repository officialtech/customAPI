from django.db import models

class Student(models.Model):
    SEX = (
        ("F", "female"),
        ("M", "male"),
        ("O", "others"),
    )
    name = models.CharField(max_length=64)
    roll_number = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    address = models.CharField(max_length=128)

    class Meta:
        verbose_name="student"
        verbose_name_plural="students"
        ordering = ["-id", "roll_number"]

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.postgres.fields import ArrayField

class Admin(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Collage(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    no_students = models.IntegerField()
    no_faculty = models.IntegerField()
    no_staff = models.IntegerField()
    departments = ArrayField(models.CharField(max_length=255))
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class FacultyAndStaff(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class KAI(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_id = models.AutoField(primary_key=True) 
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class BusinessUnit(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    phone_number = models.CharField(max_length=255)
    collage = models.ForeignKey(Collage, on_delete=models.CASCADE)
    employee = models.ForeignKey(FacultyAndStaff, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
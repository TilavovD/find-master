from django.db import models


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=64)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='district')

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SubSpeciality(models.Model):
    name = models.CharField(max_length=64)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='sub')

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(max_length=64)
    experience_year = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='master/avatar/')
    phone_number = models.CharField(max_length=13)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='master')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='master')
    address = models.CharField(max_length=128)

    specialities = models.ManyToManyField(Speciality, related_name='master')

    def __str__(self):
        return self.name


class MasterSubSpeciality(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='sub_speciality')
    sub_speciality = models.ForeignKey(SubSpeciality, on_delete=models.CASCADE, related_name='sub_speciality')
    price = models.CharField(max_length=128, default='Kelishiladi')




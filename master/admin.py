from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Master)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Speciality)
admin.site.register(SubSpeciality)
admin.site.register(MasterSubSpeciality)

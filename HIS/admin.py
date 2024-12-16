from django.contrib import admin
from .models import Admin,UserPatient,UserDoctor,Department,Order,PatientFamily
admin.site.register(Admin)
admin.site.register(UserPatient)
admin.site.register(UserDoctor)
admin.site.register(Department)
admin.site.register(Order)
admin.site.register(PatientFamily)
# Register your models here.

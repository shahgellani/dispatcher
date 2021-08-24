from django.contrib import admin

# Register your models here.


from .models import Employee, Dispatches, POD
admin.site.register(Employee)
admin.site.register(Dispatches)
admin.site.register(POD)

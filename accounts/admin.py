from django.contrib import admin

from accounts.models import User, Employee, Client

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Client)

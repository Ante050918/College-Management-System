from django.contrib import admin
from .models import UpisniList, Predmeti, Role, Status, Nositelj
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AdminNositelj(admin.StackedInline):
  model = Nositelj
  can_delete = True
  verbose_name_plural = 'Nositelj'

class AdminPredmeti(admin.ModelAdmin):
  inlines = (AdminNositelj,)
  fields = ('ime', 'kod', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni')

admin.site.register(Predmeti, AdminPredmeti)



class RoleInLine(admin.StackedInline):
    model = Role
    can_delete = True
    verbose_name_plural = 'Role'

class StatusInLine(admin.StackedInline):
    model = Status
    can_delete = True
    verbose_name_plural = 'Status'

class CustomUserAdmin(UserAdmin):
    inlines = (RoleInLine, StatusInLine,)

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
from django.forms import ModelForm
from .models import Predmeti, Nositelj, Role, Status, UpisniList
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Count
class PredmetiForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ['ime', 'kod', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni']

class NositeljForm(ModelForm):
    def __init__(self, *args, **kwargs):
      super(NositeljForm, self ).__init__(*args, **kwargs)
      self.fields['nositelj'].queryset = User.objects.filter(role__role = 'prof').annotate(prof = Count('role')).all()
    class Meta:
      model = Nositelj
      fields = ['nositelj']
        

class RoleForm(ModelForm):
    class Meta:
      model = Role
      fields = ['role']

class StatusForm(ModelForm):
    class Meta:
      model = Status
      fields = ['status']

class UpisniListForm(ModelForm):
    class Meta:
      model = UpisniList
      fields = ['predmet','status']

class UserForm(UserCreationForm):
  first_name = forms.CharField(max_length=30)
  last_name = forms.CharField(max_length=30)
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
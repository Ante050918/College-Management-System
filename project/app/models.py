from random import choices
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Predmeti(models.Model):
  IZBORNI = (('da', 'DA'), ('ne', 'NE'))
  ime = models.CharField(max_length=30)
  kod = models.CharField(max_length=30)
  program = models.TextField()
  bodovi = models.IntegerField()
  sem_redovni = models.IntegerField()
  sem_izvanredni = models.IntegerField()
  izborni = models.CharField(max_length=30, choices=IZBORNI)


class UpisniList(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
  predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE, blank = True)
  status = models.CharField(max_length=30)

  def __str__(self):
    return '%s %s %s' % (self.student, self.predmet, self.status)

class Nositelj(models.Model):
  predmeti = models.OneToOneField(Predmeti, on_delete=models.CASCADE, blank = True, null=True)
  nositelj = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)

  def __str__(self):
    return '%s %s' % (self.predmeti.ime, self.nositelj)

class Role(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  ROLE_CHOICES = [('admin', 'ADMINISTRATOR'), ('prof', 'PROFESOR'), ('stud', 'STUDENT')]
  role = models.CharField(choices = ROLE_CHOICES, max_length=30)

  def __str__(self):
    return '%s %s' % (self.user.username, self.role)


class Status(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  STATUS_CHOICES = [('red', 'REDOVNI'), ('izvan', 'IZVANREDNI')]
  status = models.CharField(choices = STATUS_CHOICES, max_length=30)

  def __str__(self):
    return '%s %s' % (self.user.username, self.status)
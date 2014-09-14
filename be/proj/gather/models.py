from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import datetime

class Point(models.Model):
  name = models.CharField(max_length=50, unique=True)
  latitude = models.FloatField()
  longitude = models.FloatField()

class UserProfile(models.Model):
  user = models.OneToOneField(User, unique=True)
  created_at = models.DateTimeField(default=datetime.now)
  location = models.ForeignKey(Point, null=True)

class Debt(models.Model):
  AUTO = 'auto'
  HOME = 'home'
  STUDENT = 'student'
  CREDIT = 'credit'
  MEDICAL = 'medical'
  OTHER = 'other'

  DEBT_CHOICES = (
    (AUTO, 'Auto'),
    (HOME, 'Home'),
    (STUDENT, 'Student'),
    (CREDIT, 'Credit'),
    (MEDICAL, 'Medical'),
    (OTHER, 'Other')
  )

  user = models.ForeignKey(User)

  # required
  kind = models.CharField(max_length=7, choices=DEBT_CHOICES)

  # optional
  amount = models.IntegerField(null=True)
  last_payment = models.DateTimeField(null=True)
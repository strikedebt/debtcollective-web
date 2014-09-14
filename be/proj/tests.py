from django.test.client import Client
from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from be.proj.gather.models import UserProfile, Debt, Point

import json


class TestSignup(TestCase):

    def test_simple(self):
      # it can create a user from the frontend
      rs = self.client.post('/signup/',
          {'username': 'test', 'password': 'anoyther'})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='test')
      self.assertEqual('test', user.username)

    def test_login(self):
      # it can login a user from the frontend
      username = 'testuser'
      password = 'testingpassword'
      rs = self.client.post('/signup/',
          {'username': username, 'password': password})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username=username)
      self.assertEqual(username, user.username)

      # bad password
      rs = self.client.post('/login/',
        {'username': username, 'password': 'this is a bad password'})
      self.assertEqual(rs.status_code, 500)

      # successful password
      rs = self.client.post('/login/',
        {'username': username, 'password': password})
      self.assertEqual(rs.status_code, 200)


    def test_points(self):
      Point.objects.create(lat=12.23, lon=-34.35, name="Albuquerque")
      Point.objects.create(lat=12.23, lon=-32.35, name="New York")
      Point.objects.create(lat=42.23, lon=-34.35, name="Newark")
      Point.objects.create(lat=12.23, lon=-31.25, name="San Francisco")

      rs = self.client.post('/points/')
      self.assertEqual(rs.status_code, 200)

      resp = json.loads(rs.content)
      self.assertEqual(len(resp), 4)
      self.assertIn('id', resp[0])
      self.assertIn('name', resp[0])
      self.assertIn('lat', resp[0])
      self.assertIn('lon', resp[0])

    def test_location(self):
      # it can store and retrieve location from the frontend
      p = Point.objects.create(lat=12.23, lon=-34.35, name="Albuquerque")
      rs = self.client.post('/signup/',
          {'username': 'testingloc',
           'password': 'testingpw',
           'location':  p.id})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc')
      self.assertEqual('testingloc', user.username)

      data = user.get_profile()
      self.assertEqual(p.id, data.location.id)

      # it turns numeric data into character
      p = Point.objects.create(lat=12.23, lon=-32.35, name="New York")
      rs = self.client.post('/signup/',
          {'username': 'testingloc2',
           'password': 'testingpw',
           'location': p.id})
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='testingloc2')
      self.assertEqual('testingloc2', user.username)

      data = UserProfile.objects.get(user=user)
      self.assertEqual(p.id, data.location.id)

    def test_debt(self):
      rs = self.client.post('/signup/',
          {'username': 'doingit',
           'password': 'testingpw',
           'kind': 'home',
           'amount': 132200
           })
      self.assertEqual(rs.status_code, 200)

      user = User.objects.get(username='doingit')
      debt = Debt.objects.get(user=user)
      self.assertEqual(debt.kind, 'home')
      self.assertEqual(debt.amount, 132200)

      # TODO: add last_payment as a viable option
      # do we use ISO or unix time?
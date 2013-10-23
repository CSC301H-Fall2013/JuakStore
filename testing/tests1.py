"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from models import *

class SprintOneTest(TestCase):
    ## Current tests are based on assumption that client is logged in.
    def setUp(self):
        c = Client()


    """
    Test if bookings are added correctly.
    """
    def test_add(self):
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00',
                                                        'end':'9:55:00', 'booker':'admin', 'room':'BA1170'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Booking.objects.filter(name='Brad Pitt', notes='test1')), 1)


    """
    Test if updating booking information works correctly.
    """
    def test_edit(self):
        original = Booking.objects.all()[0]
        original_name = original.name
        original_notes = original.notes
        response = c.post('booking/edit/1/', {'name': 'Katy Perry', 'notes': 'test2', 'category': 'stuff',
                                                         'date': '2034-12-2', 'start':'7:55:00',
                                                        'end':'9:55:00', 'booker':'admin', 'room':'BA1170'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Booking.objects.filter(name='Katy Perry', notes='test2')), 1)
        self.assertEqual(len(Booking.objects.filter(name=original_name, notes=original_notes)), 0)
        
        
    """
    Test if index page successfully renders and if all bookings are shown in the page.
    """
    def test_view(self):
        # Create an instance of a GET request.
        bookings = Booking.objects.all()
        response = c.get('/juakstore/')
        self.assertEqual(response.status_code, 200)
        for booking in bookings:
            self.assertContains(response, booking.name)
    



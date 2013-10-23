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
        self.client = Client()

    """
    Test if bookings are added correctly.
    """
    def test_add(self):
        c = Client()
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1170'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Booking.objects.filter(name='Brad Pitt', notes='test1')), 1)


    """
    Test if updating booking information works correctly.
    """
    def test_edit(self):
        c = Client()

        original = Booking.objects.all()
        original_name = Booking.name
        original_notes = Booking.notes
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
        c = Client()
        # Create an instance of a GET request.
        bookings = Booking.objects.all()
        response = c.get('/juakstore/')
        self.assertEqual(response.status_code, 200)
        for booking in bookings:
            self.assertContains(response, booking.name)

    """
    simple test example
    """
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
    

    """
    Test login response correctly
    """
    def test_d(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        check_login = self.client.login()

    """
    Test if create new account successfully.
    """
    def test_create(self):
        new_user = self.client.create('/account/create/')
        response = response = self.client.get('/account/login/')

    """
    Test if user can login in
    """
    def test_login(self):
        login_check = self.client.login(username='admin', password='JuakfrontPassword1')
        self.assertEqual(login_check,True)

    """
    Test if not every body can login to the account
    """
    def test_fail_login(self):
        login_check = self.client.login(username='', password='')
        self.assertEqual(login_check,False)

    """
    Test if rooms are added correctly.This should fail at this time
    """
    def test_addRoom(self):
        add = self.client.post('/juakstore/rooms/create/',{'Name':'new','Info':'new info'} )
        self.assertEqual(add.status_code, 200)
        self.assertEqual(Booking.name,'new')
        self.assertEqual(Booking.notes,'new info')


    """
    Test if rooms are cancelled. Need more implementation.This should fail at this time
    """
    def test_cancelRoom(self):
        delete = Delete_Room(Booking.name,'new')
        self.assertFalse(Booking.name,'new', '')


    """
    Test if clients are removed successfully.This should fail at this time
    """
    def test_remove_client(self):
        delete = Delete_client()
        self.assertFalse(Client.name,'new', '')

    """
    Test if the booking are canceled correctly.This should fail at this time
    """
    def test_cancel_booking(self):
        cancel = self.client.delete(ClientBooking.delete('new'))
        self.assertEqual(ClientBooking.client_name,'')


    """
    Test Check the list books. This should fail at this time
    """
    def test_get_booking(self):
        books = self.client.get('/juakstore/booking/')
        self.assertEqual(books.status_code, 200)
        for book in books:
            self.assertContains(book, book.name)


    """
    Test check list room. This should fail at this time
    """
    def test_get_room(self):
        rooms = self.client.get('/juakstore/rooms/')
        self.assertEqual(rooms.status_code, 200)
        for room in rooms:
            self.assertContains(room, rooms.name)





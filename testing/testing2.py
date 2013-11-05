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
    simple test example, 
    which test if the test file compile
    """
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
  
  
    """
    Test login
    This test case will test if the login page
    is responsed 
    """
    def test_d(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        check_login = self.client.login()

        
    """
    Test create new username 
    This test case will test if the test create account
    and it can get response sucessfully
    """
    def test_create(self):
        new_user = self.client.create('/account/create/')
        response = response = self.client.get('/account/login/')

    """
    Test login page
    This test case will test if people can login to the admin account
    with password admin and password JuakfrontPassword1 successfully
    """
    def test_login(self):
        login_check = self.client.login(username='admin', password='JuakfrontPassword1')
        self.assertEqual(login_check,True)

    """
    Test the login fail
    This testcase will test empty username and password will 
    drive login unsuccefully. Therefore, check not everybody 
    can login in the the page
    """
    def test_fail_login(self):
        login_check = self.client.login(username='', password='')
        self.assertEqual(login_check,False)
        
        


    """
    Test add
    This test case will test after login if user can create a booking
    with 'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
         'booker':'admin', 'room':'BA1170'
    test if bookings response sucessfully
    """
    def test_add(self):
        c = Client()
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1170'})
        self.assertEqual(response.status_code, 200)

    """
    Test add
    This test case will test after login if user can create a booking
    with 'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
          'booker':'admin', 'room':'BA1170'
    test if bookings response sucessfully 
    and the check if only one client added
    """
    def test_add(self):
        c = Client()
        response = c.post('juakstore/booking/create/', {'name': 'Susan', 'notes': 'test2', 'category': 'stuff',
                                                         'date': '2013-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA2220'})
                                                         
        self.assertEqual(len(Booking.objects.filter(name='Susan', notes='test2')), 1)
        
    """
    Test edit
    Check if the booking system responsed and user can edit the informations
    if updating booking information works correctly.
    """
    def test_edit(self):
        c = Client()

        original = Booking.objects.all()
        original_name = Booking.name
        original_notes = Booking.notes
        response = c.post('booking/edit/1/', {'name': 'Katy Perry', 'notes': 't3', 'category': 'stuff',
                                                         'date': '2034-12-2', 'start':'7:55:00',
                                                        'end':'9:55:00', 'booker':'admin', 'room':'BA1170'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Booking.objects.filter(name='Katy Perry', notes='t3')), 1)
        self.assertEqual(len(Booking.objects.filter(name=original_name, notes=original_notes)), 0)

        
    """
    Test view
    This test case will test after booking the room.
    The list of information will sucessfully shows in the website
    by compare response and booking.name
 
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
    Test add room
    This test case will chekc if rooms can be added
    with 'Name':'new','Info':'new info'
    """
    def test_addRoom(self):
        add = self.client.post('/juakstore/rooms/create/',{'Name':'new','Info':'new info'} )
        self.assertEqual(add.status_code, 200)
        self.assertEqual(Booking.name,'new')
        self.assertEqual(Booking.notes,'new info')


    """
    Test cancel Rooms
    This test case will test if a room can be removed
    with deleting the Booking.name is quals to 'new'
    """
    def test_cancelRoom(self):
        delete = Delete_Room(Booking.name,'new')
        self.assertFalse(Booking.name,'new', '')


        
    """
    Test remove client (client is partners in the manual testing)
    This test case will test if a client can be removed
    sucessfully.
    """
    def test_remove_client(self):
        delete = Delete_client('new')
        self.assertFalse(Client.name,'new', '')
        
        
    """
    Test get booking
    This test case will test if a booking can be getted by 
    compare 'new' and book.name
    Test Check the list books. This should fail at this time
    """
    def test_get_booking(self):
        books = self.client.get('/juakstore/booking/')
        self.assertEqual(books.status_code, 200)
        for book in books:
            self.assertContains('new', book.name)


        
    """
    Test cancel booking 
    This test case will test if one of the booking can be 
    cancelled sucessfully
    """
    def test_cancel_booking(self):
        cancel = self.client.delete(ClientBooking.delete('new'))
        self.assertEqual(ClientBooking.client_name,'')


        
    """
    Test schedule
    This testcase will check the schedule via a blueprint of the facility 
    sucessfully
    """
    def test_scheduled(self):
        sche = self.client.blueprint.click()
        self.assertEqual(sche.status_code, 200)
        

    """
    test get room
    This test case will check if user can get the list of rooms
    sucessfully by check rooms.names contains 'BA1180'
    """
    def test_get_room(self):
        rooms = self.client.get('/juakstore/rooms/')
        self.assertEqual(rooms.status_code, 200)
        for room in rooms:
            self.assertContains('BA1180', rooms.name)

    """
    Test weekly booking
    Check if the reapeat is 'weekly', the booking will 
    successfully booking repeatly every week
    """
    def test_weekly_booking(self):
        books = self.client.get('/juakstore/booking/')
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'start date': '2013-12-2', 'end date': '2013-12-9',
                                                         'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin','repeat':'weekly' 'room':'BA1170'})
        self.assertEqual(rooms.status_code, 200)
        self.assertContains('Brad Pitt'.date, '2013-12-2')
        self.assertContains('Brad Pitt'.date, '2013-12-9')
            
            
            

    """
    Test weekly booking
    Check if the booking successfully remove every
    week
    """
    def test_delete_weekly_booking(self):
        books = self.client.get('/juakstore/booking/')
        delete = delete_booking('Brad Pitt', 'weekly')
        self.assertFalse('Brad Pitt'.date, '2013-12-2')
        self.assertFalse('Brad Pitt'.date, '2013-12-9')
            
            
    """
    Test weekly booking
    Check if the reapeat is 'Monthly', the booking will 
    successfully booking repeatly every month
    """
    def test_monthly_booking(self):
        books = self.client.get('/juakstore/booking/')
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'start date': '2013-11-2', 'end date': '2013-11-2',
                                                         'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin','repeat':'Monthly' 'room':'BA1170'})
        self.assertEqual(rooms.status_code, 200)
        self.assertEqual('Brad Pitt'.date, '2013-11-2')
        self.assertEqual('Brad Pitt'.date, '2013-12-2')
        
    """
    Test weekly booking
    Check if the booking successfully remove every 
    month
    """
    def test_delete_montly_booking(self):
        books = self.client.get('/juakstore/booking/')
	delete = delete_booking('Brad Pitt', 'montly')
        self.assertFalse('Brad Pitt'.date, '2013-11-2')
        self.assertFalse('Brad Pitt'.date, '2013-12-2')
        
            

    """
    Test weekly booking
    Check if the reapeat is 'One-time', the booking will 
    successfully booking only one time
    """
    def test_one_booking(self):
        books = self.client.get('/juakstore/booking/')
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'start date': '2013-11-2',
                                                         'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin','repeat':'One-time' 'room':'BA1170'})
        self.assertEqual(rooms.status_code, 200)
        self.assertEqual('Brad Pitt'.date, '2013-11-2')
        self.assertFalse('Brad Pitt'.date, '2013-12-2')
        self.assertFalse('Brad Pitt'.date, '2013-12-9')
     

    """
    Test weekly booking
    Check if the reapeat is 'One-time', the booking will 
    successfully booking only one time
    """
    def test_delete_one_booking(self):
        books = self.client.get('/juakstore/booking/')
        self.assertFalse('Brad Pitt'.date, '2013-11-2')   
            
            

    """
    test book 2
    This will check the booking and cancelling 
    2 rooms for one booking is sucessfully
    """
    def test_book_2(self):
        c = Client()
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1170'})
        self.assertEqual(response.status_code, 200)
        response2 =  c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1190'})
        self.assertEqual(response2.status_code, 200)                                                

            
            
    """
    test book 3
    This will check the booking and cancelling 
    3 rooms for one booking is sucessfully
    """
    def test_book_3(self):
        c = Client()
        response = c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test1', 'category': 'stuff',
                                                         'date': '2025-12-2', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1170'})
        self.assertEqual(response.status_code, 200)
        response2 =  c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test2', 'category': 'stuff',
                                                         'date': '2025-12-4', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1190'})
        self.assertEqual(response.status_code, 200)
        response3 =  c.post('juakstore/booking/create/', {'name': 'Brad Pitt', 'notes': 'test3', 'category': 'stuff',
                                                         'date': '2025-12-3', 'start':'7:55:00', 'end':'9:55:00',
                                                         'booker':'admin', 'room':'BA1180'})
        self.assertEqual(response3.status_code, 200)                                                

            
        
    """
    Test cancel booking 
    Booking and cancelling all rooms for one booking is sucessful
    """
    def test_cancel_booking(self):
        cancel = self.client.delete(ClientBooking.delete('Brad Pitt','all'))
        self.assertEqual(ClientBooking.client_name,'')


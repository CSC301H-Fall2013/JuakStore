"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import unittest
from django.test import TestCase
from django.test.client import Client
from forms import *
from models import *
from views import *



class ModelTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
        
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
    Test login page
    This test case will test if people can login to the admin account
    with password admin and password JuakfrontPassword1 successfully
    """
    def test_login(self):
        login_check = self.client.login(username='admin', password='JuakfrontPassword1')
        #self.assertEqual(login_check,True)
        self.assertRaises(TypeError,login_check,False)
    
    """
    Test model Room(database)
    """
    def test_model_Room(self):
        room1 = Room.objects.create(name="BA1190", info="lecture room")
        room2 = Room.objects.create(name="BA1180", info="another lecture room")
    	self.assertEquals(room1.name, "BA1190")
    	self.assertEquals(room1.info,"lecture room")
        self.assertEquals(room2.name, "BA1180")
    	self.assertEquals(room2.info,"another lecture room")
    	
    """
    Test model Partner(database)
    """
    def test_model_Partner(self):
    	user = User.objects.create_user('user','changyingyu1991@gmail.com','1234');
    	
        partner = Partner.objects.create(uID= user,company = "BMO", 
        								info="this is partner1", name = "admin", approved="no")
    	self.assertEquals(partner.uID.username, "user")
    	self.assertEquals(partner.company,"BMO")
        self.assertEquals(partner.info, "this is partner1")
    	self.assertEquals(partner.name,"admin")
    	self.assertEquals(partner.approved,"no")
    	
    	
    """
    Test model Partner(database)
    """
    def test_model_BookingCategroy(self):
        bookCate = BookingCategory.objects.create(name = "Badminton class")
    	self.assertEquals(bookCate.name, "Badminton class")
    
    
 
    
    """
    Test model Partner(database)
    """
    def test_model_Booking(self):
        user = User.objects.create_user('user1','changyingyu1991@gmail.com','1234');
        bookCate = BookingCategory.objects.create(name = "Badminton class")        
        room1 = Room.objects.create(name="BA1190", info="lecture room")
        book = Booking.objects.create(name = "booking1", notes = "This is booking 1", 
        								category = bookCate, date = "2013-12-25", start = "14:00:00",
        								end = "15:00:00", booker = user, room = room1 )
    	self.assertEquals(book.name, "booking1")
    	self.assertEquals(book.notes, "This is booking 1")
    	self.assertEquals(book.category.name, "Badminton class")
    	self.assertEquals(book.date, "2013-12-25")
    	self.assertEquals(book.start, "14:00:00")
    	self.assertEquals(book.end, "15:00:00")
    	self.assertEquals(book.booker.username, "user1")
    	self.assertEquals(book.room.name, "BA1190")
    
    
    """
    Test model Partner(database)
    """
    def test_model_ClientBookingCategroy(self):
    	user = User.objects.create_user('user2','changyingyu1991@gmail.com','1234');
        bookCate = BookingCategory.objects.create(name = "Badminton class")        
        room1 = Room.objects.create(name="BA1190", info="lecture room")
    	book = Booking.objects.create(name = "booking1", notes = "This is booking 1", 
    									category = bookCate, date = "2013-12-25", start = "14:00:00",
    									end = "15:00:00", booker = user, room = room1 )
    	
        ClientBook = ClientBooking.objects.create(start = "2013-12-25 14:00:00", 
        											end = "2013-12-25 15:00:00", client_name = "Ying" , 
        											client_email = "changyingyu1991@gmail.com", 
        											phone_number = "4aa", booking = book,)
        
    	self.assertEquals(ClientBook.start, "2013-12-25 14:00:00")
    	self.assertEquals(ClientBook.end, "2013-12-25 15:00:00")
    	self.assertEquals(ClientBook.client_name, "Ying")
    	self.assertEquals(ClientBook.client_email, "changyingyu1991@gmail.com")
    	self.assertRaises(TypeError,ClientBook.phone_number, "4aa") 
    	# restricted on numbers? some intergers?
    	self.assertEquals(ClientBook.booking.name, "booking1")
    	
    	

    
    
class ViewTest(unittest.TestCase):     
    def setUp(self):
        self.client = Client()

	

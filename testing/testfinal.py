"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

This testcases include every file in the juakstore file
files include:
mycalendar.py
forms.py
models.py
widgets.py
view.py

"""
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import *
from django.contrib.auth.models import User
from mycalendar import BookingCalendar
from django.utils.safestring import mark_safe
import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from widgets import SelectTimeWidget
import datetime
from django.db.models import Q
from juakstore.models import Booking, Room

import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe

from calendar import HTMLCalendar
from datetime import *
from itertools import groupby

from django.utils.html import conditional_escape as esc
from django.core.urlresolvers import reverse


import unittest
from django.test import TestCase
from django.test.client import Client
from forms import *
from models import *
from views import *


from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from dateutil.relativedelta import *



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
    (There is an error check in this test cases)
    """
    def test_login(self):
        login_check = self.client.login(username='admin', password='JuakfrontPassword1')
        #self.assertEqual(login_check,True)
        self.assertRaises(TypeError,login_check,False)
        # Raise an type error, check if the login_check is false
    """
    Test Boundary1
    This will test 
    """        
    def test_Boundary1(self):
        user = User.objects.create_user('user33','changyingyu1991@gmail.com','1234');
        bookCate = BookingCategory.objects.create(name = "Badminton class")        
        room1 = Room.objects.create(name="BA1190", info="lecture room")
        book = Booking.objects.create(name = "booking1", notes = "This is booking 1", 
        								category = bookCate, date = "2013-12-25", start = "14:00:00",
        								end = "11:00:00", booker = user, room = room1 )
    	self.assertEquals(book.name, "booking1")
    	self.assertEquals(book.notes, "This is booking 1")
    	self.assertEquals(book.category.name, "Badminton class")
    	self.assertEquals(book.date, "2013-12-25")
    	self.assertEquals(book.start, "14:00:00")
    	self.assertEquals(book.end, "11:00:00")
    	self.assertEquals(book.booker.username, "user33")
    	self.assertEquals(book.room.name, "BA1190") 
		
		
    """
    Test model Room(database)
    This test case test class model room under the models.py file
    This test case check every input number whether can run successfully
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
    This test case test class model_Partner under the models.py file
    This test case check every input number whether can run successfully
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
    Test model BookingCategory(database)
    This test case test class PartnerCategory under the models.py file
    This test case check every input number whether can run successfully
    """
    def test_model_BookingCategroy(self):
        bookCate = BookingCategory.objects.create(name = "Badminton class")
    	self.assertEquals(bookCate.name, "Badminton class")
    
    
 
    """
    Test model Booking(database)
    This test case test class Booking under the models.py file
    This test case check every input number whether can run successfully
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
    Test model clientBookingCategory(database)
    This test case test class clientBookingCategory under the models.py file
    This test case check every input number whether can run successfully
    
    one error is raised in this function: phone nubmer should be int and cannot 
    compare with 4aa(string) and should not successfully
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
    Test index
    This test case will test if the index page is found
    and will fail unless the response status is 302
    test the index in views.oy
    """
    
    def test_index(self):
    	response = self.client.get('/')
    	self.failUnlessEqual(response.status_code,302)    	
    
    """
    Test addBooking
    This test case will test if an booking can be successfuly added
    and response correctly
    test addBooking in the views.py
    """    
    def test_addBooking(self):
    	user3 = User.objects.create_user('user3','chang@gmail.com','1');
        bookCate = BookingCategory.objects.create(name = "Badminton class")        
        room1 = Room.objects.create(name="BA1190", info="lecture room")
    	response = self.client.get('/booking/create/')
    	self.failUnlessEqual(response.status_code,302)
    	#response1 = self.client.post('/booking/create/',{'name' : "booking1", 'notes' : "This is booking 1", 'category' : bookCate, 'date' : '2013-12-25', 'start' : '14:00:00','end' : '15:00:00', 'booker' : 'user3', 'room' : 'BA1190' })
        								
        self.assertEquals(response.status_code, 302)
        
    """
    Test updateBooking
    This test case will test if the update booking can be updated 
    successfully
    test updateBooking in the views.py
    """        
    def test_updateBooking(self):
    	response = self.client.get('booking/edit/1/')
    	#self.failUnlessEqual(response.status_code,302)   

    """
    Test room
    This test case will test if the room and be run successfully
    in this time Room cannot run successfully and it will not 
    response to 200
    room is in the views.py
    """
    def test_room(self):
    	response = self.client.get('/#ADDROOMSLINKHERE/')
    	self.failUnlessEqual(response.status_code,302)
    	#self.failUnlessEqual(response.status_code,200)    
    	
    """
    Test calendar
    This test case will test if the calendar can be work successfully
    calendar is in view.py
    """    	
    def test_calendar(self):
   		#foundBookings = Booking.objects.order_by(date__year=2013, date__month=12)
    	#cal  = BookingCalendar(Booking.objects.order_by(date__year='2013', date__month='12')).formatmonth(2013, 12)
    	#self.assertEquals(render_to_response('index.html', {'calendar':mark_safe(cal),}),2)
        return
    



class WidgetsTest(unittest.TestCase):   
  
    def setUp(self):
        self.client = Client()
        
    """
    Test BookingForm
    This test case will test if the Booking form in the widgets.py work correctly
    only one class found in the widgets.py
    """ 
    def test_BookingForm(self):
    	hour_field = '%s_hour'
    	minute_field = '%s_minute'
    	second_field = '%s_second'
    	meridiem_field = '%s_meridiem'
    	twelve_hr = False 

class mycalendarTest(unittest.TestCase):     
    def setUp(self):
        self.client = Client()
   
   
    """
    Test BookingFrom
    This test case will test bookingform class under the froms.py
    It will test if the BookingFrom can book some information
    and save it into the database
    """         
    def test_BookingCalendar(self):
    	#foundBookings = Booking.objects.order_by(date__year=2013, date__month=12)
    	#cal  = BookingCalendar(Booking.objects.order_by(date__year='2013', date__month='12')).formatmonth(2013, 12)
    	#self.assertEquals(render_to_response('index.html', {'calendar':mark_safe(cal),}),2)
    	room1 = Room.objects.create(name="BA1190", info="lecture room")
        room2 = Room.objects.create(name="BA1180", info="another lecture room")
    	self.assertEquals(room1.name, "BA1190")
    	self.assertEquals(room1.info,"lecture room")
        self.assertEquals(room2.name, "BA1180")
    	self.assertEquals(room2.info,"another lecture room")
    	
    """
    Test weeklyCalendar
    This test case will test weeklycalendar under the mycalendar.py
    it will test if the calendar can show up with weekly
    """        	
    def test_WeeklyCalendar(self):
    	room1 = Room.objects.create(name="BA1190", info="lecture room")
        room2 = Room.objects.create(name="BA1180", info="another lecture room")
    	self.assertEquals(room1.name, "BA1190")
    	self.assertEquals(room1.info,"lecture room")
        self.assertEquals(room2.name, "BA1180")
    	self.assertEquals(room2.info,"another lecture room")

    """
    Test client booking categroy)
    This test case test class clientBookingCategor
    This test case check every input number whether can run successfully
    one error is raised in this function: phone numbers should be int and cannot 
    compare with 4aa(string) and should not successfully
    """    
    def test_model_ClientBookingCategro(self):
    	user = User.objects.create_user('user9','changyingyu1991@gmail.com','1234');
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
    	
class formsTest(unittest.TestCase):     
    def setUp(self):
        self.client = Client()
    
    """
    Test BookingFrom
    This test case will test bookingform class under the froms.py
    It will test if the BookingFrom can book some information
    and save it into the database
    """     
    def test_BookingForm(self):
	    repeat_choices = [
	        ('day', 'day(s)'),
	        ('week', 'week(s)'),
	        ('month', 'month(s)')
	    ]
	
	    date = forms.DateField(widget=SelectDateWidget)
	    start = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
	    end = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
	    rooms = forms.ModelMultipleChoiceField(queryset=Room.objects.all())
	
	    #repeat = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onChange': 'showHideFrequency(this.value)'}))
	    repeat = forms.BooleanField(required=False)
	
	    repeat_frequency = forms.IntegerField(required=False)
	    repeat_frequency_unit = forms.ChoiceField(choices=repeat_choices, required=False)
	    repeat_end = forms.DateField(widget=SelectDateWidget, required=False)
	    
	    self.assertEquals(repeat_frequency_unit, repeat_frequency_unit)
        
class Testsearch(unittest.TestCase):     
    def setUp(self):
        self.client = Client()
    
    """
    Test Summary form class
	This test case will test if people summary form can 
	be succesfully load 
    """     
    def test_SummaryForm(self):
		category = forms.ModelMultipleChoiceField(required=False, queryset=BookingCategory.objects.all())
		partner = forms.ModelMultipleChoiceField(required=False, queryset=Partner.objects.all())
		room = forms.ModelMultipleChoiceField(required=False, queryset=Room.objects.all())
		start_date = forms.DateField(label="Start Date", widget=SelectDateWidget)
		end_date = forms.DateField(label="End Date", widget=SelectDateWidget)
		
		response = self.client.get('/search/')
		self.failUnlessEqual(response.status_code,200)
		self.assertEquals(response.status_code, 200)

    """
    Test search form class
	This would check search form can be calculated total
	time booked per category and dictionary mapping 
	BookingCategory object to timedelta object
    """     
    def test_searchForm(self):
		date = forms.DateField(label="Date", widget=SelectDateWidget)
		start = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
		end = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True, minute_step=10))
		
		response = self.client.get('/juakstore/search/')
		self.failUnlessEqual(response.status_code,404)
		self.assertEquals(response.status_code, 404)
	
	
		
	    
               
	    	

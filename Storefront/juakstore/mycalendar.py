from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc



'''
    Credit to: http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
'''

class BookingCalendar(HTMLCalendar):

    def __init__(self, bookings):
        super(BookingCalendar, self).__init__()
        self.bookings = self.group_by_day(bookings)
        print self.bookings

    def formatday(self, day, weekday):
        print day
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.bookings:
                cssclass += ' filled'
                body = ['<ul>']
                for booking in self.bookings[day]:
                    body.append('<li>')
                    #body.append('<a href="%s">' % booking.get_absolute_url())
                    body.append(esc(booking.name))
                    body.append('</li>')
                    #body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(BookingCalendar, self).formatmonth(year, month)

    def group_by_day(self, bookings):
        field = lambda booking: booking.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(bookings, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
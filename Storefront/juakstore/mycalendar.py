from calendar import HTMLCalendar
from datetime import date, timedelta
from itertools import groupby

from django.utils.html import conditional_escape as esc
from django.core.urlresolvers import reverse


'''
    Credit to: http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
'''

class BookingCalendar(HTMLCalendar):

    def __init__(self, bookings):
        super(BookingCalendar, self).__init__()
        self.bookings = self.group_by_day(bookings)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.bookings:
                cssclass += ' filled'
                body = ['<div id="tribe-events-content" class="tribe-events-month"><div id="tribe-events-header" data-title="Events this {{month}}"><ul class="tribe-events-sub-nav">']
                body.append('<ul>')
                for booking in self.bookings[day]:
                    body.append('<li class="cal-list">')
                    body.append(' <h3 class="tribe-events-month-event-title summary"><a href="%s" class="url calendar-list">' % reverse('juakstore:bookingDetail', None, [booking.id]))
                    body.append(esc(booking.name))
                    body.append('</a></h3></li>')
                body.append('</ul></ul></div></div>')
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



class WeeklyCalendar():
    cssclass = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun']
    tableheader = "<table class=\"week tribe-events-calendar\">" \
                  "<thead>" \
                  "<tr>" \
                  "<th id=\"tribe-events-monday\" >Monday</th>" \
                  "<th id=\"tribe-events-tuesday\" >Tuesday</th>" \
                  "<th id=\"tribe-events-wednesday\" >Wednesday</th>" \
                  "<th id=\"tribe-events-thursday\" >Thursday</th>" \
                  "<th id=\"tribe-events-friday\" >Friday</th>" \
                  "<th id=\"tribe-events-saturday\" >Saturday</th>" \
                  "<th id=\"tribe-events-sunday\" >Sunday</th>" \
                  "</tr>" \
                  "</thead>" \
                  "<tbody class=\"hfeed vcalendar\">"

    def __init__(self, bookings):
        self.bookings = self.group_by_day(bookings)

    def group_by_day(self, bookings):
        field = lambda booking: booking.date
        return dict(
            [(day, list(items)) for day, items in groupby(bookings, field)]
        )

    def formatweek(self, year, month, day):

        weekHTML = self.tableheader

        basedate = date(year, month, day)
        # first find out which day of the week it is, 0 is Monday, 6 is Sunday
        day_of_week = basedate.weekday()

        start_of_week = basedate - timedelta(days=day_of_week)

        for i in range(0, 7):
            weekHTML += self.formatday(start_of_week, i)
        weekHTML += '</tbody></table>'
        return weekHTML

    '''
        Given the start_of_week as a date object, and the day_of_week as an integer
        with 0 as Monday, 6 as Sunday, outputs the cell corresponding to this day in the
        weekly view
    '''
    def formatday(self, start_of_week, day_of_week):
        cssclass = self.cssclass[day_of_week]
        current_day = start_of_week + timedelta(days=day_of_week)

        body = ['<div id="tribe-events-daynum-']
        body.append(str(current_day.day))
        body.append('">')
        body.append(str(current_day.day))
        body.append('</div>')

        if current_day == date.today():
            cssclass += ' today'

        if current_day in self.bookings:
            cssclass += ' filled'
            body.append('<div class="hentry vevent tribe-events-vategory-jobs post-1395 tribe_events type-tribe-events status-publish">')
            for booking in self.bookings[current_day]:
                body.append('<h3 class="tribe-events-month-event-title summary">')
                body.append('<a href="%s" class="url">' % reverse('juakstore:bookingDetail', None, [booking.id]))
                body.append(esc(booking.name))
                body.append('</a>')
                #body.append('<div class="starttime">')
                #body.append(str(booking.start))
                #body.append('</div>')
                body.append('</h3>')
            body.append('</div></div>')
            print body
            return self.day_cell(cssclass, ''.join(body))
        print body
        return self.day_cell(cssclass, ''.join(body))



    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)



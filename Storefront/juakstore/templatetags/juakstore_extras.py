from django import template
from juakstore.models import Booking
from juakstore.mycalendar import BookingCalendar, WeeklyCalendar
from django.utils.safestring import mark_safe


register = template.Library()

@register.tag(name="calendar")
def populate_calendar(parser, token):
    try:
        tag_name, booking_set, year, month = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag requires 3 arguments")
    return CalendarNode(booking_set, year, month)

class CalendarNode(template.Node):
    def __init__(self, booking_set, year, month):
        self.booking_set = template.Variable(booking_set)
        self.year = template.Variable(year)
        self.month = template.Variable(month)

    def render(self, context):
        foundBookings = self.booking_set.resolve(context).order_by('date')\
            .filter(date__year=self.year.resolve(context), date__month=self.month.resolve(context))
        cal  = BookingCalendar(foundBookings).formatmonth(self.year.resolve(context), self.month.resolve(context))
        return mark_safe(cal)

@register.tag(name="agenda")
def populate_week_agenda(parser, token):
    try:
        tag_name, booking_set, year, month, day = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag requires 4 arguments")
    return WeekAgendaNode(booking_set, year, month, day)

class WeekAgendaNode(template.Node):
    def __init__(self, booking_set, year, month, day):
        self.booking_set = template.Variable(booking_set)
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.day = template.Variable(day)

    def render(self, context):
        foundBookings = self.booking_set.resolve(context).order_by('date')\
            .filter(date__year=self.year.resolve(context), date__month=self.month.resolve(context))
        agenda = WeeklyCalendar(foundBookings).formatweek(self.year.resolve(context),
                                                          self.month.resolve(context),
                                                          self.day.resolve(context))
        print agenda
        return mark_safe(agenda)
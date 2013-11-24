__author__ = 'wyeung'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from juakstore import views
from juakstore import search

urlpatterns = patterns('',
                    url(r'^$', views.index, name='index'),
                    url(r'^public/$', views.publicView, name='publicView'),
                    url(r'^adminview/$', views.adminView, name='adminView'),
                    url(r'^adminview/partner/(?P<pk>\w+)/$', views.accept, name='adminAccept'),
                    url(r'^adminview/partner/decline/(?P<pk>\w+)/$', views.decline, name='adminDecline'),
                    url(r'^adminview/booking/(?P<pk>\w+)/$', views.acceptBooking, name='adminAcceptBooking'),
                    url(r'^adminview/booking/decline/(?P<pk>\w+)/$', views.declineBooking, name='adminDeclineBooking'),
                    url(r'^conflict/(?P<pk>\d+)/$', views.display_conflics, name='conflictDetail'),
                    url(r'^delete/(?P<pk>\d+)/$', views.deleteBooking, name='deleteBooking'),
                    url(r'^logout/$', views.logoutStorefront, name='logout'),
                    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.index, name='indexyymm'),
                    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.index, name='indexyymm'),
                    url(r'^booking/(?P<pk>\d+)/$', views.displayBooking, name='bookingDetail'),
                    url(r'^booking/create/$', login_required(views.BookingCreate.as_view()), name='bookingCreate'),
                    url(r'^booking/create/(?P<year>\d+)/(?P<month>\d+)/$', login_required(views.BookingCreate.as_view()), name='bookingCreateyymm'),
                    url(r'^booking/edit/submit/(?P<pk>\d+)/$', views.updateBooking, name='submitBooking'),
                    url(r'booking/create/submit/$', views.addBooking, name='bookingSubmit'),
                    url(r'^booking/edit/(?P<pk>\d+)/$', staff_member_required(views.BookingUpdate.as_view()), name='editBooking'),
                    url(r'^users/(?P<pk>\d+)/$', login_required(views.UserDetailView.as_view()), name='userDetail'),
                    url(r'^rooms/$', login_required(views.RoomList.as_view()), name='roomList'),
                    url(r'^rooms/create/submit/$', views.submitRoom, name='roomSubmit'),
                    url(r'^rooms/create/$', login_required(views.RoomCreate.as_view()), name='roomCreate'),
                    url(r'^rooms/(?P<pk>\d+)/$', login_required(views.RoomView.as_view()), name='roomDetail'),
                    url(r'^rooms/(?P<pk>\d+)/date/(?P<year>\d+)/(?P<month>\d+)/$', login_required(views.BookingView.as_view()), name='roomDetailyymm'),
                    url(r'^search_booking/$', search.search_booking, name='search_booking')
)

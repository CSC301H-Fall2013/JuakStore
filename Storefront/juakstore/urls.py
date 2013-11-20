__author__ = 'wyeung'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from juakstore import views
from juakstore import search

urlpatterns = patterns('',
                    url(r'^$', views.index, name='index'),
                    url(r'^adminview/$', views.adminView, name='adminView'),
                    url(r'^logout/$', views.logoutStorefront, name='logout'),
                    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.index, name='indexyymm'),
                    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.index, name='indexyymm'),
                    url(r'^booking/(?P<pk>\d+)/$', views.displayBooking, name='bookingDetail'),
                    url(r'^booking/create/$', login_required(views.BookingCreate.as_view()), name='bookingCreate'),
                    url(r'^booking/create/(?P<year>\d+)/(?P<month>\d+)/$', login_required(views.BookingCreate.as_view()), name='bookingCreateyymm'),
                    url(r'^booking/edit/submit/(?P<pk>\d+)/$', views.updateBooking, name='submitBooking'),
                    url(r'booking/create/submit/$', views.addBooking, name='bookingSubmit'),
                    url(r'^booking/edit/(?P<pk>\d+)/$', login_required(views.BookingUpdate.as_view()), name='editBooking'),
                    url(r'^users/(?P<pk>\d+)/$', login_required(views.UserDetailView.as_view()), name='userDetail'),
                    url(r'^rooms/$', login_required(views.RoomList.as_view()), name='roomList'),
                    url(r'^rooms/create/submit/$', views.submitRoom, name='roomSubmit'),
                    url(r'^rooms/create/$', login_required(views.RoomCreate.as_view()), name='roomCreate'),
                    url(r'^rooms/(?P<pk>\d+)/$', login_required(views.RoomView.as_view()), name='roomDetail'),
                    url(r'^rooms/(?P<pk>\d+)/date/(?P<year>\d+)/(?P<month>\d+)/$', login_required(views.BookingView.as_view()), name='roomDetailyymm'),
                    
                    # testing search
                    (r'^search/$', search.search_form),
)
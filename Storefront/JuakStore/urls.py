__author__ = 'wyeung'
from django.conf.urls import patterns, url

from juakstore import views

urlpatterns = patterns('',
                    url(r'^$', views.index, name='index'),
                    url(r'^booking/(?P<pk>\d+)/$', views.BookingView.as_view(), name='bookingDetail'),
                    url(r'^booking/create/$', views.BookingCreate.as_view(), name='bookingCreate'),
                    url(r'booking/create/submit/', views.addBooking, name='bookingSubmit'),
                    url(r'^booking/edit/(?P<pk>\d+)/$', views.BookingUpdate.as_view(), name='editBooking'),
                    url(r'^booking/edit/submit/(?P<pk>\d+)/$', views.updateBooking, name='submitBooking'),
                    url(r'^users/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='userDetail'),
)
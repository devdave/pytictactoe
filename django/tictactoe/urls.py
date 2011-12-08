from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { 'template' : 'index.html'} ),
    url(r'^move/(?P<x>\d+)/(?P<y>\d+)$', 'game.views.move', name = "Move"),
    url(r'^reset$', 'game.views.init', name = "Move"),
    url(r'^init$', 'game.views.init', name = "Move"),
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^tictactoe/', include('tictactoe.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

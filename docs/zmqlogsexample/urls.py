from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'zmqlogsexample.views.home', name='home'),
)


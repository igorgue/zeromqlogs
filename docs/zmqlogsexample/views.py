import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

log = logging.getLogger(__name__)  # Get an instance of a logger

def home(request):
    if request.method == 'GET':
        c = RequestContext(request, {})

        return render_to_response('home.html', c)

    log_type = request.POST.get('type')
    message = request.POST.get('message')

    getattr(log, log_type)(message, extra={'request': request})

    log_text = "{0} log successful: '{1}'".format(log_type.upper(), message)
    if log_type == 'debug':
        messages.success(request, log_text)
    if log_type == 'critical':
        messages.error(request, log_text)
    else:
        getattr(messages, log_type)(request, log_text)

    return HttpResponseRedirect('/')


import logging

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

    return HttpResponseRedirect('/')


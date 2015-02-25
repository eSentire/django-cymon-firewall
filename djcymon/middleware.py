"""Django middlewares."""

import urllib2
from django.conf import settings
from django.http import Http404
from django.utils import simplejson

CYMON_BASE_API_URL = getattr(settings, 'CYMON_BASE_API_URL', 'http://cymon.io/api/public/nexus')

class CymonFirewallMiddleware(object):
    """Serve 404 responses to IP addresses that are found in Cymon's database.

    .. note::
        This will only take effect if ``settings.DEBUG`` is False.

    .. note::
        You can also disable this middleware when testing by setting
        ``settings.CYMON_FIREWALL_DISABLE`` to True.
    """
    def process_request(self, request):
        # If the user has explicitly disabled SSLify, do nothing.
        if getattr(settings, 'CYMON_FIREWALL_DISABLE', settings.DEBUG):
            return None

        # If we get here, proceed as normal.
        remote_address = None
        if request.META.get('REMOTE_ADDR', '') not in ['127.0.0.1', '0.0.0.0', '', None]:
            remote_address = request.META['REMOTE_ADDR']
        if request.META.get('HTTP_X_FORWARDED_FOR', '') not in ['127.0.0.1', '0.0.0.0', '', None]:
            # always override 'REMOTE_ADDR' if this header exists
            remote_address = request.META['HTTP_X_FORWARDED_FOR']
        if remote_address:
            try:
                data = urllib2.urlopen("%s?%s" %(CYMON_BASE_API_URL, remote_address)).read()
                res = simplejson.loads(data)
                if res.get('status') == 200 and res.get('is_reported') is True:
                    return Http404('Request Blocked')
            except:
                pass
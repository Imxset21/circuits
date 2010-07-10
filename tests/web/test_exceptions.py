#!/usr/bin/env python

from urllib2 import urlopen, HTTPError

from circuits.web import Controller
from circuits.web.exceptions import *

"""
BadGateway
BadRequest
Forbidden
Gone
InternalServerError
LengthRequired
MethodNotAllowed
NotAcceptable
NotFound
NotImplemented
PreconditionFailed
RequestEntityTooLarge
RequestTimeout
RequestURITooLarge
ServiceUnavailable
Unauthorized
UnicodeError
UnsupportedMediaType
"""

class Root(Controller):

    def test_forbidden(self):
        raise Forbidden()

    def test_notfound(self):
        raise NotFound()

def test_forbidden(webapp):
    from circuits import Debugger
    Debugger(events=False).register(webapp)

    try:
        urlopen("%s/test_forbidden" % webapp.server.base)
    except HTTPError, e:
        assert e.code == 403
        assert e.msg == "Forbidden"
    else:
        assert False

def test_notfound(webapp):
    try:
         urlopen("%s/test_notfound" % webapp.server.base)
    except HTTPError, e:
        assert e.code == 404
        assert e.msg == "Not Found"
    else:
        assert False

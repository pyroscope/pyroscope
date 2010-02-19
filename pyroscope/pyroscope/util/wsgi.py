""" PyroScope - WSGI Tools.

    Copyright (c) 2009 The PyroScope Project <pyroscope.project@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import time

from webob import Request


class LatencyProfilingMiddleware(object):
    """ Measure the execution time of any request and add
        the result into the body, by replacing a special token.
    """
    
    # MIME types supported in addition to "text/*" and "*+xml"
    SUPPORTED_MIME_TYPES = (
        "application/xml", "application/json", "application/jsonrequest",
    )
    
    # Unique text that gets replaced with the timing result
    TOKEN = "<!-- LATENCY_PROFILING_RESULT -->"

        
    def __init__(self, app, config=None):
        """ Initialize profiling filter with wrapped application.
        """
        self.app = app
        self.config = config or {}


    def __call__(self, environ, start_response):
        """ Clock the execution time of this request.
        """
        # TODO Check a config switch and delegate directly to app if disabled.
        start_time = time.time()
        request = Request(environ)
        response = request.get_response(self.app)

        filtering = (response.content_type.startswith("text/")
            or response.content_type.endswith("+xml")
            or response.content_type in self.SUPPORTED_MIME_TYPES
        )

        if filtering:
            # Report timing result
            # TODO This isn't exactly a performance-minded implementation!
            latency = time.time() - start_time
            runtime = "%d sec(s) %.1f msecs" % (int(latency), latency * 1000.0 % 1000)
            response.body = response.body.replace(self.TOKEN, runtime)

        return response(environ, start_response)


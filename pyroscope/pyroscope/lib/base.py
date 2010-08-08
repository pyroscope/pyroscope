""" PyroScope - The base Controller API.

    Provides the BaseController class for subclassing.

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

from pylons import request, config, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from pyrocore.util import fmt
from pyrocore.util.types import Bunch
from pyroscope.engines import rtorrent


class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """ Invoke the Controller.
        """
        c._messages = []

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)


class PageController(BaseController):

    GLOBAL_STATE = {
        "max_up_rate":      "get_upload_rate",
        "max_down_rate":    "get_download_rate",
        "max_up_slots":     "get_max_uploads_global",
        "max_down_slots":   "get_max_downloads_global",
        "max_http":         "get_max_open_http",
        "max_sockets":      "get_max_open_sockets",
        "max_files":        "get_max_open_files",
        "max_mem":          "get_max_memory_usage",
        "dht_port":         "get_dht_port",
    }


    def __init__(self):
        self.proxy = rtorrent.Proxy.create()


    def __call__(self, environ, start_response):
        """ Invoke the Controller.
        """
        c._debug = []
        c._timezone = config['pyroscope.timezone']

        c.engine = Bunch()
        c.engine.startup = fmt.human_duration(rtorrent.get_startup(), precision=3)

        #XXX Use multimethod, or get from poller
        for attr, method in self.GLOBAL_STATE.items():
            c.engine[attr] = getattr(self.proxy.rpc, method)()

        return BaseController.__call__(self, environ, start_response)


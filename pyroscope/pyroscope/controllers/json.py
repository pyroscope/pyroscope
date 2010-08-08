""" PyroScope - Controller "json".

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
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from pyroscope.lib.base import render, BaseController
from pyroscope.engines import rtorrent

log = logging.getLogger(__name__)


class JsonController(BaseController):
    """ The JSON API.
    """
    # Methods in here should usually delegate to other modules preparing the data!

    @jsonify
    def engine_state(self):
        """ Return global state of torrent engine, mainly for updating
            the header display.
        """
        return dict(
            engine = rtorrent.get_global_state(),
            clock = int(time.time()),
        )            


    def index(self):
        # Redirect to lab index page
        return redirect_to(controller="sandbox", action="index", id="json")


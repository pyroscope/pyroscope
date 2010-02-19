""" PyroScope - The application's Globals object.

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

import logging

from pyroscope.engines import rtorrent
from pyroscope.util.types import Bunch

LOG = logging.getLogger(__name__)


class Globals(Bunch):
    """ Globals acts as a container for objects available throughout the
        life of the application
    """

    def __init__(self):
        """ One instance of Globals is created during application
            initialization and is available during requests via the
            'app_globals' variable
        """
        self.engine_id = "Unknown Engine ID"
        try:
            proxy = rtorrent.Proxy()
            self.engine_id = "%s [%s]" % (proxy.id, proxy.version)
            self.xmlrpc_bug = proxy.rpc.system.time_usec() < 0
        except Exception, exc:
            LOG.warning("Cannot determine engine ID (%s)" % exc)
        

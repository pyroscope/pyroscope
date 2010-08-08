""" PyroScope - Controller "admin".

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
from __future__ import with_statement

import os
import logging
from contextlib import closing
from collections import defaultdict

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pyrocore.util.algo import product
from pyrocore.util.types import Bunch

from pyroscope.lib.base import render, PageController
from pyroscope.engines import rtorrent

log = logging.getLogger(__name__)


class AdminController(PageController):

    VIEWS = (
        Bunch(action="config", icon="cog.12 View Configuration Files", title="Show Config"),
        Bunch(action="log", icon="file.12 View Log Files", title="Show Logs"),
    )


    def __init__(self):
        self.proxy = rtorrent.Proxy.create()
        self.views = dict((view.action, view) for view in self.VIEWS)


    def __before__(self):
        # Set list of views
        c.views = self.VIEWS


    def _render(self):
        return render("/pages/admin.mako")


    def config(self):
        c.view = self.views['config']

        # Build search path
        session_dir = self.proxy.rpc.get_session()
        cur_dir = self.proxy.rpc.system.get_cwd()
        search_path = []
        for path in (session_dir, os.path.dirname(session_dir.rstrip(os.sep)), cur_dir, "~"):
            path = os.path.expanduser(path.rstrip(os.sep))
            if path not in search_path:
                search_path.append(path)

        # Find rtorrent.rc file
        for path, name in product(search_path, ("rtorrent.rc", ".rtorrent.rc")):
            c.filename = os.path.join(path, name)
            if os.path.exists(c.filename):
                break
        else:
            c.filename = None
            c._messages.append("Cannot find rTorrent configuration file in %s!" % ', '.join(search_path))

        # Load file
        if c.filename:
            with closing(open(c.filename, "r")) as handle:
                c.lines = handle.readlines()

        return self._render()


    def log(self):
        c.view = self.views['log']
        c.filename = "N/A"
        c.lines = []

        return self._render()


    def index(self):
        # Redirect to config file view
        ##return self._render()
        ##return redirect_to(action="config")
        return self.config()


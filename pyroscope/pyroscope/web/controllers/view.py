""" PyroScope - Controller "view".

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
from fnmatch import fnmatchcase as fnmatch

from paste.deploy.converters import asbool
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pyroscope.web.lib.base import render, PageController
from pyroscope.util import fmt
from pyroscope.util.types import Bunch
from pyroscope.engines import rtorrent

log = logging.getLogger(__name__)


def _make_state(item):
    """ Generate string torrent states.
    """
    yield "OPEN" if item.is_open else "CLOSED"
    yield "DONE" if item.complete else "INCOMPLETE"
    if item.message: yield "MSG"
    yield "PRV" if item.is_private else "PUB"


def make_tooltip(item):
    """ Make a tooltip from the most important torrent details.
    """
    lines = [
        ##"HASH: %s" % item.hash,
        "RATIO: %.3f" % (item.ratio / 1000.0,),
        "RATE UP/DN: %s / %s" % (fmt.human_size(item.up_rate), fmt.human_size(item.down_rate)),
        "XFER UP/DN: %s / %s" % (fmt.human_size(item.up_total), fmt.human_size(item.down_total)),
        "STATE: %s" % " ".join(_make_state(item)),
        # last state change?
    ]

    return u"\n\u00A0|\u00A0".join(lines)


class ViewController(PageController):

    IGNORE_MESSAGES = [
        "Timeout was reached",
        "Tried all trackers",
        "Could not parse bencoded data",
        "Couldn't connect to server",
    ]
    VIEWS = (
        Bunch(action="active", title="Active", icon="nuked.12", stock=False),
        Bunch(action="incomplete", title="Incomplete", icon="box-cross.12"),
        Bunch(action="stopped", title="Stopped", icon="stopped.12"),
        Bunch(action="hashing", title="Hashing", icon="hash.12"),
        Bunch(action="name", title="Loaded", icon="torrent.12"),
        #Bunch(action="main", title="Loaded"),
        Bunch(action="complete", title="Completed", icon="box-check.12"),
        Bunch(action="seeding", title="Seeding", icon="green_up_single.12"),
        Bunch(action="started", title="Started", icon="started.12"),
    )


    def __init__(self):
        self.proxy = rtorrent.Proxy()
        self.views = dict((view.action, view) for view in self.VIEWS)


    def __before__(self):
        # Set list of views
        c.views = self.VIEWS

        # Set flags
        c.refresh_rate = request.params.get("refresh", 60)
        c.obfuscate = asbool(request.params.get("_obfuscate", request.params.get("_obfuscated")))
        c.filter_mode = request.params.get("filter_mode", "AND")


    def _get_messages(self, torrents):
        """ Get messages from a list of torrents.
        """
        if asbool(request.params.get("_debug")) and torrents:
            torrents[0].message += " [FAKE MESSAGE FOR TESTING]"

        return [Bunch(hash=item.hash, name=item.name, text=item.message, 
                tooltip=make_tooltip(item),
                domains=", ".join(sorted(item.tracker_domains)))
            for item in torrents 
            if item.is_open and item.message and not any(ignore in item.message
                for ignore in self.IGNORE_MESSAGES
            )
        ]


    def _model_fixup(self):
        """ Go through c.torrents and fix up the items; also do some stats.
        """
        c.up_total, c.down_total = 0, 0
        for item in c.torrents:
            c.up_total += item.up_rate
            c.down_total += item.down_rate

            ##d.get_peers_accounted()
            ##d.get_peers_connected()
            ##d.get_peers_max()
            ##d.get_peers_min()
            ##d.get_peers_not_connected() 
            #XXX This seems reliable only for active torrents
            item.seeders = item.peers_complete + (item.is_open and item.complete)
            item.leeches = (item.peers_not_connected + item.peers_connected
                - item.peers_complete + (item.is_open and not item.complete))

            item.tooltip = make_tooltip(item)
            item.ratio_not0 = item.ratio / 1000.0 or 1E-12
            item.domains = ", ".join(item.tracker_domains)

            # XXX Fix bug in XMLRPC (using 32bit integers?)
            if item.size_bytes < 0:
                item.size_bytes = (item.size_chunks-1) * item.chunk_size + item.size_bytes % item.chunk_size
            if item.down_total < 0 and item.up_total > 0:
                item.down_total = int(item.up_total / item.ratio_not0)
            elif item.down_total > 0 and item.up_total < 0:
                item.up_total = int(item.down_total * item.ratio_not0)

        c.messages = self._get_messages(c.torrents)

        """ XXX stats code currently not used!
        
        domains = set(domain for item in all_torrents for domain in item.tracker_domains)
        active_up = [item for item in c.torrents if item.up_rate and not item.down_rate]
        active_down = [item for item in c.torrents if not item.up_rate and item.down_rate]
        active_both = [item for item in c.torrents if item.up_rate and item.down_rate]
        ratios = [item.ratio for item in all_torrents if item.down_total or item.up_total]
        #queued = [item for item in all_torrents if not (item.down_total or item.up_total)]
        seeds = [item for item in all_torrents if not item.down_total and item.up_total]

        counts = {}
        for attr in ("is_open", "complete"):
            counts[attr] = sum(getattr(item, attr) for item in all_torrents)
        """

            
    def _get_active(self):
        """ Get active torrents.
        """
        # Filter & decorate, sort, undecorate
        return [i for _, _, i in sorted([
            (item.up_rate, item.down_rate, item) 
            for item in rtorrent.View(self.proxy, "main").items()
            if item.down_rate or item.up_rate
        ], reverse=True)]


    def _filter(self, torrents, query):
        """ Filter list of torrents.
        """
        def fields(item):
            "Which fields to search in..."
            yield item.name
            for i in item.tracker_domains:
                yield i.lstrip("*.")
            for i in _make_state(item):
                yield i

        if query:
            patterns = ["*%s*" % p if '*' not in p else p
                for p in query.lower().split()]

            # AND: all patterns must be matched
            # OR:  at least 1 pattern must be matched
            threshold = len(patterns) if c.filter_mode == "AND" else 1

            return [item for item in torrents
                if threshold <= sum(
                    any(fnmatch(i.lower(), p) for i in fields(item))
                    for p in patterns
                )
            ]
        else:
            return torrents


    def _normalized_filter(self):
        """ Normalize filter query.
        """
        filter = request.params.get("filter", "").lower()
        if filter == "filter...":
            filter = ""
        return ' '.join(["%s*" % p if '*' not in p and '[' not in p else p
            for p in filter.split()
        ])


    def list(self, id):
        c.view = self.views[id]

        # Get list of torrents
        if c.view.get("stock", True):
            # Built-in view
            c.torrents = list(rtorrent.View(self.proxy, id).items())
        else:
            # Handle non-stock views
            c.torrents = getattr(self, "_get_" + id)()
        
        # Handle filter
        c.torrents_unfiltered = len(c.torrents)
        c.filter = self._normalized_filter()
        c.torrents = self._filter(c.torrents, c.filter)

        # Build view model
        self._model_fixup()
        
        # Return a rendered template
        return render("pages/view.mako")


    def index(self):
        # Redirect to list of active torrents
        ##return redirect_to(action="list", id="active")
        return self.list("active")


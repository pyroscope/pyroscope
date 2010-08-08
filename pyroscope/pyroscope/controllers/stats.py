""" PyroScope - Controller "stats".

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
from collections import defaultdict

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from pyrocore.util.types import Bunch

from pyroscope.lib.base import render, PageController
from pyroscope.engines import rtorrent

log = logging.getLogger(__name__)


def domain_key(item):
    return ", ".join(i.lstrip(".*") for i in sorted(item.tracker_domains))

def get_tracker_stats(torrents):
    """ Sum up different values per tracker, over all torrents.
    """
    tracker_stats = {}
    for item in torrents:
        domain = domain_key(item)
        tracker_stats.setdefault(domain, defaultdict(int))
        tracker_stats[domain]["loaded"] += 1
        tracker_stats[domain]["done" if item.complete else "incomplete"] += 1
        tracker_stats[domain]["open" if item.is_open else "closed"] += 1
        tracker_stats[domain]["prv" if item.is_private else "pub"] += 1
        if item.down_rate or item.up_rate:
            tracker_stats[domain]["active"] += 1
        tracker_stats[domain]["up"] += max(0, item.up_total)
        tracker_stats[domain]["down"] += max(0, item.down_total)
        tracker_stats[domain]["ratio"] += item.ratio / 1000.0
        if item.size_bytes > 0:
            tracker_stats[domain]["size"] += item.size_bytes
        if item.down_total:
            tracker_stats[domain]["down_count"] += 1
            tracker_stats[domain]["real_ratio"] += item.ratio / 1000.0

    # Do totals over all fields
    totals = defaultdict(int)
    for values in tracker_stats.values():
        for key, val in values.items():
            totals[key] += val

    return tracker_stats, totals


class StatsController(PageController):

    VIEWS = (
        Bunch(action="trackers", icon="tracker.12 Torrent Stats per Tracker", title="Trackers"),
    )


    def __init__(self):
        self.proxy = rtorrent.Proxy()
        self.views = dict((view.action, view) for view in self.VIEWS)


    def __before__(self):
        # Set list of views
        c.views = self.VIEWS


    def _render(self):
        return render("/pages/stats.mako")


    def trackers(self):
        # XXX: do this in the __before__, need to find out the action name though
        c.view = self.views['trackers']

        # Get list of torrents
        torrents = list(rtorrent.View(self.proxy, "main").items())

        #c.domains = set(domain for item in torrents for domain in item.tracker_domains)
        #c.active_up = [item for item in torrents if item.up_rate and not item.down_rate]
        #c.active_down = [item for item in torrents if not item.up_rate and item.down_rate]
        #c.active_both = [item for item in torrents if item.up_rate and item.down_rate]
        #c.ratios = [item.ratio for item in torrents if item.down_total or item.up_total]
        #c.seeds = [item for item in torrents if not item.down_total and item.up_total]

        #c.counts = {}
        #for attr in ("is_open", "complete"):
        #    c.counts[attr] = sum(getattr(item, attr) for item in torrents)

        # Sum up different values per tracker, over all torrents
        c.trackers, c.totals = get_tracker_stats(torrents)

        return self._render()


    def index(self):
        # Redirect to list of active torrents
        ##return self._render()
        ##return redirect_to(action="trackers")
        return self.trackers()


# -*- coding: utf-8 -*-
""" PyroScope - Controller "sandbox".

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

import os
import time
import logging
from cgi import escape
from collections import defaultdict

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from pyrocore.util.types import Bunch
from pyroscope.web.lib.helpers import obfuscate, bibyte
from pyroscope.web.lib.base import render, PageController
from pyroscope.web.controllers.json import JsonController
from pyroscope.web.controllers.view import make_tooltip
from pyroscope.engines import rtorrent

log = logging.getLogger(__name__)



def shorten(text, maxlen=40, tail=5):
    """ Shorten a text to a maximal length.
    """
    if len(text) > maxlen:
        text = text[:maxlen - 3 - tail] + "..." + text[-tail:]
    return text


def quoted(text):
    """ Put text in quotes.
    """
    return u"«%s»" % text


class SandboxController(PageController):

    VIEWS = {
        "yui": "YUI",
        "jit": "JIT",
        "ohloh": "ohloh.net",
        "icons": "Icons",
        "json": "JSON",
        "globals": "Globals",
        "request": "Request",
        "helpers": "Helpers",
        "sandbox": "Sandbox",
        "timeline": "Timeline",
        "rtorrent": "rTorrent",
    }
    
    # Time span in seconds for hot spots
    BUCKET_SIZE = 240

    # Minimum number of events considered a hotspot
    HOTSPOT_SIZE = 10

    rt_globals = (
        'dht_statistics', 
        ##'false',
        'get_bind',
        'get_check_hash',
        'get_connection_leech',
        'get_connection_seed',
        'get_dht_port',
        'get_directory',
        'get_down_rate',
        'get_down_total',
        'get_download_rate',
        'get_max_downloads_div',
        'get_max_downloads_global',
        'get_max_file_size',
        'get_max_memory_usage',
        'get_max_open_files',
        'get_max_open_http',
        'get_max_open_sockets',
        'get_max_peers',
        'get_max_peers_seed',
        'get_max_uploads',
        'get_max_uploads_div',
        'get_max_uploads_global',
        'get_memory_usage',
        'get_min_peers',
        'get_min_peers_seed',
        'get_name',
        'get_peer_exchange',
        'get_port_open',
        'get_port_random',
        'get_port_range',
        'get_safe_free_diskspace',
        'get_send_buffer_size',
        'get_session',
        'get_session_lock',
        'get_stats_not_preloaded',
        'get_stats_preloaded',
        ##'get_tracker_dump',
        'get_up_rate',
        'get_up_total',
        'get_upload_rate',
        'get_use_udp_trackers',
        'get_xmlrpc_size_limit',
        'system.client_version',
        'system.get_cwd',
        'system.hostname',
        'system.library_version',
        'system.pid',
        'system.time',
        'system.time_seconds',
        'system.time_usec',
        'view_list',
    )
    

    def __before__(self):
        self.now = time.localtime(time.time())
        c.now = time.strftime("%c", self.now)


    @jsonify
    def jit(self):
        ##import copy
        from math import log
        from pyroscope.web.controllers.stats import domain_key, get_tracker_stats

        # Get rTorrent proxy and a torrents list
        proxy = rtorrent.Proxy()
        torrents = list(rtorrent.View(proxy, 'main').items())
        tracker_stats, totals = get_tracker_stats(torrents)

        # Create root node
        root = Bunch(
            id = "root",
            name = proxy.id,
            data = {"$area": 100},
            children = [],  
        )
        
        # Add tracker hierarchy
        trackers = set(domain_key(item) for item in torrents)
        trackers_node = dict(
            id = "trackers",
            name = "Data Size per Tracker",
            data = {"$area": 50},
            children = [{
                    "id": "trk-%s" % tracker.replace('*', '_').replace('.', '-')
                        .replace(',', '').replace(' ', ''),  
                    "name": "%s [%d / %s / %.1f%%]" % (
                        tracker, tracker_stats[tracker]["loaded"],
                        bibyte(tracker_stats[tracker]["size"]),
                        100.0 * tracker_stats[tracker]["size"] / totals["size"],
                    ),
                    "data": {
                        ##"$area": tracker_stats[tracker]["loaded"] or 1,
                        "$area": tracker_stats[tracker]["size"],
                        "$color": int(100 * log(max(1, 100 * tracker_stats[tracker]["size"] // totals["size"])) / log(100)),
                    },  
                    "children": [],    
                }
                for tracker in sorted(trackers)
            ],  
        )
        root.children.append(trackers_node)

        def copy_children(scope, children):
            for item in children:
                item = item.copy()
                item["id"] = "%s-%s" % (scope, item["id"])
                yield item

        # Status selection
        status_node = dict(
            id = "status",
            name = "Status",
            data = {"$area": 50},
            children = [{
                    "id": "status-%s" % status,  
                    "name": "%s [%d]" % (status, totals[status]),
                    "data": {"$area": totals[status] or 1},  
                    "children": [], ##list(copy_children(status, trackers_node["children"])),
                }
                for status in ('active', 'done', 'incomplete', 'open', 'closed', 'prv', 'pub')
            ],  
        )
        ##root.children.append(status_node)

        # Recurse over tree and add areas
        def area_sum(tree):
            area = 0
            for node in tree["children"]:
                if "$area" not in node["data"]:
                    area_sum(node)
                area += node["data"]["$area"]

            tree["data"]["$area"] = area
            return tree
        
        # Return graph data
        return area_sum(root)

    
    def data(self, id):
        if id == "timeline.xml":
            response.headers['Content-Type'] = 'application/xml; charset="utf-8"'

            proxy = rtorrent.Proxy.create()
            torrents = list(rtorrent.View(proxy, 'main').items())
            torrent_data = []
            rtorrent_start = rtorrent.get_startup()

            span_data = defaultdict(list)
            for item in torrents:
                title = shorten(obfuscate(item.name))
                if item.is_open:
                    # Store in minute-sized buckets
                    span_data[item.state_changed // self.BUCKET_SIZE * self.BUCKET_SIZE].append(item)
                elif item.message:
                    # Add closed torrents with a message (like unregistered ones)
                    torrent_data.append(u'<event start="%s" title="Stopped %s">'
                            u'Stopped %s, possibly due to %s @ %s</event>' % (
                        time.strftime("%c", time.localtime(item.state_changed)),
                        escape(quoted(title), quote=True),
                        escape(quoted(obfuscate(item.name))),
                        escape(quoted(item.message)),
                        ", ".join(escape(obfuscate(i)) for i in item.tracker_domains),
                    ))

                tied_file = os.path.expanduser(item.tied_to_file)
                if os.path.exists(tied_file):
                    torrent_data.append(u'<event start="%s" title="Downloaded %s">'
                            u'Downloaded metafile for %s</event>' % (
                        time.strftime("%c", time.localtime(
                            os.path.getmtime(tied_file)
                        )),
                        escape(quoted(title), quote=True),
                        escape(quoted(obfuscate(item.name))),
                    ))

            for bucket, items in span_data.items():
                if len(items) > self.HOTSPOT_SIZE:
                    # hot spot, f.x. happens when you restart rTorrent
                    # since we filtered open torrents only, they had to be started at that point
                    entries = [Bunch(
                        title = u"Started %d torrents within %d secs, seeding them..." % (
                            len(items), self.BUCKET_SIZE),
                        start = bucket,
                        text = ",\n".join(shorten(obfuscate(item.name), 20) for item in items[:40])
                             + (", ..." if len(items) > 40 else ""),
                    )]
                else:
                    # torrent gets its own event
                    entries = [Bunch(
                            title = u"%s %s" % (
                                u"Seeding" if item.complete else u"Leeching",
                                quoted(shorten(obfuscate(item.name))) ),
                            start = item.state_changed,
                            text = u"NAME: %s | %s" % (
                                obfuscate(item.name), make_tooltip(item)),
                        ) for item in items
                    ]

                torrent_data.extend([u'<event start="%s" end="%s" title="%s">%s</event>' % (
                        time.strftime(u"%c", time.localtime(entry.start)),
                        c.now,
                        escape(entry.title, quote=True),
                        escape(entry.text),
                    ) for entry in entries
                ])

            if rtorrent_start:
                torrent_data.append(u'<event start="%s" title="rTorrent started"></event>' % (
                    time.strftime(u"%c", time.localtime(rtorrent_start)),
                ))

            torrent_data.append(u'<event start="%s" title="The time is now %s"></event>' % (
                c.now, time.strftime("%Y-%m-%d %H:%M:%S", self.now),
            ))

            torrent_data = u'\n'.join(torrent_data)

            return u"""<?xml version="1.0" encoding="utf-8"?>
<data>""" + torrent_data + u"""
    <event 
            start="Jun 04 2009 00:00:00 GMT"
            title="PyroScope project created on Google Code"
            image="http://code.google.com/p/pyroscope/logo?logo_id=1245201363"
        ><![CDATA[
            Initial directory structure for project 
            <a href="http://pyroscope.googlecode.com/">PyroScope</a> 
            created in SVN.
        ]]>
    </event>
    
    <!--    
    <event 
            start="Jun 13 2009 00:00:00 GMT"
            title="Started rTorrent 0.8.2/0.12.2"
        >
        Started rTorrent 0.8.2/0.12.2
    </event>
    
    <event 
            start="Jun 14 2009 22:00:00 GMT"
            end="Jun 16 2009 01:00:00 GMT"
            isDuration="true"
            title="Downloading Debian.ISO"
        >
        Debian.ISO [3333MiB, Ratio 1.234]
        </event>
        
    <event 
            start="Jun 16 2009 01:00:00 GMT"
            end="Jun 20 2009 14:00:00 GMT"
            isDuration="true"
            title="Seeding Debian.ISO"
        >
        Debian.ISO [3333MiB, Ratio 2.674]
        </event>
        
    <event link="...">
    -->
</data>
"""


    def index(self, id=None):
        c.views = self.VIEWS
        c.view = id if id in c.views else sorted(c.views)[0]
        c.title = c.views[c.view]
        c.rt_globals = self.rt_globals
     
        if c.view == "icons":
            c.icons = sorted(os.path.splitext(name)[0]
                for name in os.listdir(os.path.join(os.path.dirname(__file__), "../public/img/svg/icons"))
                if name.endswith(".svg")
            )
        elif c.view == "rtorrent":
            c.proxy = rtorrent.Proxy()
            if request.params.get("methods"):
                c.methods = defaultdict(list)
                for method in c.proxy.rpc.system.listMethods():
                    c.methods[method[0].upper()].append((method, (
                        c.proxy.rpc.system.methodSignature(method), 
                        c.proxy.rpc.system.methodHelp(method),
                    )))
        elif c.view == "json":
            c.json_api = dict((method, getattr(getattr(JsonController, method), '__doc__'))
                for method in dir(JsonController)
                if not method.startswith('_') 
                and method != 'index'
                and callable(getattr(JsonController, method))
            )

        # Return a rendered template
        return render("pages/sandbox.mako")


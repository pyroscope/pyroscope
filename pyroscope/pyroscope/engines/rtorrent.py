""" PyroScope - rTorrent Interface.

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
import socket
import xmlrpclib
from fnmatch import fnmatch
from urlparse import urlparse
from xml.parsers.expat import ExpatError as XmlParseError

from pyroscope import config
from pyroscope.util import xmlrpc2scgi
from pyroscope.util.types import Bunch


# Create alias so clients don't have to import xmlrpclib
Error = xmlrpclib.Error

class TorrentAttributeError(Error, AttributeError):
    """ Attribute not found.
    """


GLOBAL_STATE_FIELDS = dict(
    up_rate = "get_up_rate",
    down_rate = "get_down_rate", 
    #up_slots = "", 
    #down_slots = "",
    #http = "",
    #sockets = "",
    #files = "",
    mem = "get_memory_usage",
    dht = "dht_statistics",
)

def get_global_state():
    fields = GLOBAL_STATE_FIELDS.items()
    args = [{'methodName': method, 'params': []} for _, method in fields]
    results = Proxy.create().rpc.system.multicall(args)
    
    return dict((key, val[0])
        for (key, _), val in zip(fields, results)
        if isinstance(val, (list, tuple)) # else it's a fault!
    )



def get_startup():
    proxy = Proxy.create()
    rtorrent_start = None
    if proxy.rpc.get_session_lock():
        lock_file = os.path.join(proxy.rpc.get_session(), "rtorrent.lock")
        if os.path.exists(lock_file):
            rtorrent_start = os.path.getmtime(lock_file)
    return rtorrent_start


class Proxy(object):

    instance = None

    @classmethod
    def create(cls):
        # XXX: Thread-safety?!
        if cls.instance is None:
            cls.instance = Proxy()
        return cls.instance

    def __init__(self):
        self.rpc = xmlrpc2scgi.RTorrentXMLRPCClient(config.scgi_url)
        try:
            self.id = self.rpc.get_name()
        except socket.error, exc:
            raise Error("Can't connect to %s (%s)" % (config.scgi_url, exc))

        self.version = "rTorrent %s/%s" % (
            self.rpc.system.client_version(), self.rpc.system.library_version(),
        )
        self.session_dir = self.rpc.get_session()
        self.download_dir = os.path.expanduser(self.rpc.get_directory())


class Download(Bunch):

    IMMUTABLE = set((
        "hash", "name", "is_private", "tracker_size", 
    ))
    PRE_FETCH = IMMUTABLE | set((
        "base_path", "tied_to_file", 
        "is_open", "complete",
        "ratio", "up_rate", "up_total", "down_rate", "down_total",
    ))


    def __init__(self, proxy, values=None):
        dict.__setattr__(self, "proxy", proxy)
        Bunch.__init__(self, values)

 
    def __getitem__(self, name):
        if name not in self:
            # On demand attribute access
            if name == "tracker_urls":
                value = [self.proxy.rpc.t.get_url(self["hash"], i) for i in range(self["tracker_size"])]
            elif name == "tracker_domains":
                value = set(("." + urlparse(url)[1].split(":")[0])
                        .replace(".tracker.",".*.")
                        .replace(".Tracker.",".*.")
                        .replace(".update.",".*.")
                        .replace(".announce.",".*.")
                        .replace(".www.",".*.")
                        .lstrip("1234567890.")
                    for url in self.tracker_urls)
                value.discard('')
            else:
                accessor = ("" if name.startswith("is_") else "get_") + name
                try:
                    value = getattr(self.proxy.rpc.d, accessor)(self["hash"])
                except Error, exc:
                    raise TorrentAttributeError("Attribute %r not available (%s)" % (name, exc))
            self[name] = value # cache it for later access
            return value
        else:
            return Bunch.__getitem__(self, name)


    def __getattr__(self, name):
        try:
            return Bunch.__getattr__(self, name)
        except AttributeError:
            return self[name]


    def clear(self):
        immutable = dict((key, val) for (key, val) in self.items() if key in self.IMMUTABLE)
        Bunch.clear(self)
        self.update(immutable)


    def dump(self):
        print self.name
        print " ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.creation_date))
        print " ", self.base_path
        print " ", os.path.expanduser(self.tied_to_file)
        print " ", os.path.join(self.proxy.session_dir, self.hash + ".torrent")
        print " ", self.tracker_urls


    def domain_match(self, domain_patterns):
        return any(fnmatch(domain, pattern)
            for pattern in domain_patterns
            for domain in self.tracker_domains)


class View(object):
    """ Object representing a named rTorrent view.
    """

    def __init__(self, proxy, name):
        self.proxy = proxy
        self.name = name


    def items(self):
        args = [self.name] + ["d.%s%s=" % (
                "" if field.startswith("is_") else "get_", field
            ) for field in Download.PRE_FETCH]
        for item in self.proxy.rpc.d.multicall(*tuple(args)):
            yield Download(self.proxy, zip(Download.PRE_FETCH, item))


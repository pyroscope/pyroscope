""" PyroScope - Background Demon Thread.

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
from collections import defaultdict

from pyroscope.util.types import Bunch
from pyroscope.engines import rtorrent

LOG = logging.getLogger(__name__)


# TODO An actual implementation
class RefreshPoller(object):
    """ The RefreshPoller is a demon thread that refreshes the list of
        all downloads periodically.
    """
    
    # How long to sleep between refreshes, all other times are measured in ticks
    # (this allows to easily fine-tune system load vs. up-to-dateness using only one value)
    CLOCK_TICK = 1.0 # secs

    # How often to refresh mutable values
    MUTABLE_TICKS = 1

    # How often to refresh the list of download hashes (i.e. recognize deletions / additions)
    HASH_LIST_TICKS = 10
    
    # How often to get the full list of values (to fix out-of-sync problems and
    # get fresh almost-immutable values like download locations)
    SYNC_TICKS = 60

    # How long to sleep (at max) after problems, i.e. unknown exceptions
    PENALTY_TICKS = 1
    MAX_PENALTY_TICKS = 15

    # How long to keep deletions around [minutes]
    DELETION_RETENTION = 5

    
    def __init__(self):
        """ Initialize the refresh poller.
        """
        self.proxy = rtorrent.Proxy()
        self.shutdown = False
        self.downloads = {}
        self.deleted = defaultdict(list)
        self.ticks = 0
        self.penalty = 0

        # refreshed never -- or actually 1970 ;)
        self.now = 0
        self.last_update = 0.0
        self.last_sync = 0.0


    def _deleted(self, id_hash):
        """ Register a hash as deleted.
        """
        # Keep a reference and remove from downloads
        item = self.downloads[id_hash]
        del self.downloads[id_hash]

        # Append to deletion buffer
        item.last_update = self.now
        self.deleted[self.now // 60].append(item)


    def _sync(self):
        """ Do a full sync.
        """
        try:
            downloads = dict((item.hash, item) 
                for item in rtorrent.View(self.proxy, "main")
            )
        except rtorrent.Error:
            LOG.exception("Problem while syncing...")
        else:
            # Record deletions!
            deleted = set(self.downloads) - set(downloads)
            for hash in deleted:
                self._deleted(hash)

            self.downloads = downloads
            self.last_update = self.last_sync = time.time()

        # Prune deletions buffer
        now_mins = self.now // 60
        for bucket in self.deleted:
            if bucket + self.DELETION_RETENTION < now_mins:
                del self.deleted[bucket]


    def _hash_list(self):
        """ Get a new hash list.
        """
        #XXX Implement!
        # Consider deletions!


    def _mutables(self):
        """ Refresh mutable values.
        """
        for item in self.downloads:
            pass #XXX Implement!
            # Consider deletions!


    def _mainloop(self):
        """ Refresh poller mainloop.
        """
        LOG.info("refresh poller started...")

        while not self.shutdown:
            try:
                self.now = time.time()

                if self.ticks % self.SNYC_TICKS == 0:
                    self._sync()
                elif self.ticks % self.HASH_LIST_TICKS == 0:
                    self._hash_list()
                elif self.ticks % self.MUTABLE_TICKS == 0:
                    self._mutables()
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                self.penalty = min(self.penalty + self.PENALTY_TICKS, self.MAX_PENALTY_TICKS)
                LOG.exception("Unknown problem in refresh poller, resuming...")
            else:
                self.penalty = 0
                self.last_updated = self.now

            time.sleep(self.CLOCK_TICK * (self.penalty + 1))
            self.ticks += 1

        LOG.info("refresh poller shutting down...")


    def run(self):
        """ Start the refresh poller thread.
        """
        #XXX Implement!


    def updated_since(self, timestamp):
        """ Generate a list of all items updated since a certain point in time.
        
            This is used to get the browser up-to-date via AJAX.
        """
        #XXX need to keep record of deletions  for a while and somehow transfer them
        if self.now > timestamp:
            #XXX Need ThreadLock for this block?
            downloads = self.downloads

            # Yield loaded downloads (unless deleted in the meantime by poller)
            sent = set(downloads)
            for id_hash in sent:
                item = downloads.get(id_hash)
                if item and item.last_updated > timestamp:
                    yield item

            # Send deletions; note that hashes can be reloaded, so we need to
            # filter what we have! Also, we need to go through time in reverse and
            # send each hash only once!
            #XXX Implement!

        # else generator is simply empty


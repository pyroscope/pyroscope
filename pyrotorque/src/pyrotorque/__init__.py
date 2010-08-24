""" PyroCore - Python Torrent Tools Core Package.

    Copyright (c) 2010 The PyroScope Project <pyroscope.project@gmail.com>

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

# TODO: cyclic refresh
#   - config param "update_cycle" for length of update cycle (in sec)
#   - get initial list of hashes
#   - get bursts of hashes, each "update_cycle / burst_size" secs
#   - watch "active" and "incomplete" view and update those more frequently (list of "hot" hashes)
#   - if hash disappears (i.e. we get a xmlrpc fault), remove hash from list
#   - do a full referesh of the list of hashes from time ti time (once each cycle?)
#
#   - put list of hashes we change into "dirty" list
#   - re-get dirty hashes on read access

# TODO: simple web interface
#   - wsgiref server
#   - status page with:
#       * other general stats (AJAX down/up bandwidth update, etc.)
#       * recent log lines
#       * in-memory debug log
#   - stop / restart demon
#   - pyrrd data display


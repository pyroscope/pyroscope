""" PyroScope - Routes Configuration.

    The more specific and detailed routes should be defined first so they
    may take precedent over the more generic routes. For more information
    refer to the routes manual at http://routes.groovie.org/docs/

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

from pylons import config
from routes import Mapper


def make_map():
    """ Create, configure and return the routes Mapper.
    """
    map = Mapper(directory=config["pylons.paths"]["controllers"],
                 always_scan=config["debug"])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect("/error/{action}", controller="error")
    map.connect("/error/{action}/{id}", controller="error")

    # CUSTOM ROUTES HERE

    # Default routes
    map.connect("/{controller}", action="index")
    map.connect("/{controller}/{action}")
    map.connect("/{controller}/{action}/{id}")

    # Define root page
    map.connect("/", controller="index", action="index")

    # Always remove trailing slash
    map.redirect('/*(url)/', '/{url}', _redirect_code='301 Moved Permanently')

    return map


""" PyroScope - Web Helper Functions.

    Consists of functions to typically be used within templates, but also
    available to Controllers. This module is available to templates as 'h'.

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

import re

from paste.deploy.converters import asbool
from pylons.controllers.util import url_for
from webhelpers.html import literal
#from webhelpers.html.tags import checkbox, password


def icon(name):
    """ Emit image tag for an icon.
    """
    title = ""
    if ' ' in name:
        name, title = name.split(None, 1)
        title = 'title="%(title)s" alt="%(title)s" ' % locals()

    size = 24
    if '.' in name:
        name, size = name.split('.')
        size = int(size)

    return literal('<img src="/img/png/%(size)d/%(name)s.png" height="%(size)d" width="%(size)d" %(title)s/>') % locals()


def img(name):
    """ Emit tag for a general image.
    
        "name" is expected to be a string like ImageMagick's "indentify" emits it.
    """
    name, title, size = name.split()
    if title in ("PNG", "GIF", "JPG"):
        title = ""
    else:
        title = title.replace("_", " ")
        title = 'title="%(title)s" alt="%(title)s" ' % locals()
    w, h = size.split("x")
    return literal('<img src="/img/%(name)s" height="%(h)s" width="%(w)s" %(title)s/>') % locals()


def bibyte(val):
    """ Format numerical byte size as human size.
    """
    from pyrocore.util.fmt import human_size

    try:
        val = int(val)
    except (TypeError, ValueError):
        return val
    else:    
        return human_size(val)


def obfuscate(text, replacer=re.compile("[a-zA-Z<>&]+")):
    """ Obfuscator for screenshots and the like. Replaces all alpha chars by question marks.
    """
    from pylons import request

    obfuscate = asbool(request.params.get("_obfuscate", request.params.get("_obfuscated")))
    return replacer.sub(lambda s: "?" * len(s.group()), text) if obfuscate else text


def echo(url, view_params=None, form=False):
    """ Add existing query parameters to an URL.
    """
    from pylons import request

    view_params = view_params or ()
    params = []
    
    # Helper variable to check for already existing URL parameters
    check_url = url.replace('?', '&')
    
    # Find parameters we want to echo
    for key, val in request.params.items():
        if (key in view_params or key.startswith('_')) and ('&'+key+'=') not in check_url:
            params.append((key, val))

    # Add any parameters found    
    if params:
        if form:
            import cgi

            url = literal(''.join('<input type="hidden" name="%s" value="%s" />' % (
                    cgi.escape(key, quote=True), cgi.escape(val, quote=True)
                ) for key, val in params
            ))
        else:
            import urllib
            
            url += '?' if '?' not in url else '&'
            url += urllib.urlencode(params)

    return url


def nowrap(text):
    """ Replace all spaces by non-breakable ones.
    """
    return text.replace(u' ', u'\u00A0')


def nostrip(text):
    """ Replace all leading and trailing spaces by non-breakable ones.
    """
    stripped = text.strip()
    if stripped is not text:
        l = len(text) - len(text.lstrip())
        t = len(text) - len(text.rstrip())
        text = u'\u00A0' * l + text + u'\u00A0' * t
    return text


def now():
    """ Return current time as a string.
    """
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


# not needed anymore
del re


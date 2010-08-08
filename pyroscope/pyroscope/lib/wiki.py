""" PyroScope - Read-only Google Code Wiki Handling.

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
import re
import logging
from cgi import escape

from webhelpers.html import literal

LOG = logging.getLogger(__name__)


class WikiPage(object):
    """ Handle a Google Code wiki page. It's just intended to display the help pages,
        so it has very little error handling and doesn't support complex layout 
        combinations (for example, list items should not span several lines).

        Most problems should be fixed by editing the faulty pages, before changing 
        the code here and making it more complex. See SimpleMarkup in the wiki for
        the exact rules and samples.
    """

    # Directory holding the pages
    WIKI_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wiki")

    # URL to create wanted pages
    EDIT_URL = "http://code.google.com/p/pyroscope/w/edit/"

    # Regular expressions for inline markup parsing
    RE_CAPS = re.compile(r"([A-Z])") # used to split the title into words
    RE_INLINE = re.compile('|'.join([
        r"\*(?P<strong>.*?)\*",
        r"_(?P<em>.*?)_",
        r"`(?P<code>.*?)`",
        r"{{{(?P<tt>.*?)}}}",
        r"(?P<img>https?://.+?/.+?\.(?:png|gif|jpg|jpeg))",
        r"\[(?P<urlb>https?://.+?/.+?\s.+?)\]",
        r"(^|(?<!\w))(?P<urli>https?://([^\s\<%(punct)s]|([%(punct)s][^\s\<%(punct)s]))+)" % {
            "punct": re.escape('''"\'}]|:,.)?!'''),
        },
        r"(?P<a>(?:[A-Z][a-z0-9_]+){2,32})",
    ]))


    @classmethod
    def open(cls, name):
        """ Open page from file.
        """
        page_file = os.path.join(cls.WIKI_ROOT, name + ".wiki")
        handle = open(page_file, "r")
        try:
            return cls(name, handle.read())
        finally:
            handle.close()


    def __init__(self, name, raw):
        """ Initialize & parse wiki page object.
        """
        self.name = name
        self.raw = raw
        self.title = self.RE_CAPS.sub(r" \1", name).strip()
        self.lines = []
        self.meta = {}
        self.html = u''

        self._parse()


    def _exists(self, name):
        """ Check if named page exists
        """
        return os.path.isfile(os.path.join(self.WIKI_ROOT, name + ".wiki"))


    def _metadata(self):
        """ Parse meta data at the top
        """
        while self.lines and self.lines[0].startswith("#"):
            key, val = self.lines[0][1:].split(None, 1)
            self.meta[key] = val
            self.lines = self.lines[1:]


    def _inline(self):
        """ Handle inline markup. Markup CAN NOT span several lines, and it 
            probably can't be nested!
        """
        def replacer(match):
            "Substitution helper"
            #return repr(match.groupdict())

            # Assemble text for the simple cases where group name == tag name
            text = ''.join("<%s>%s</%s>" % (name, text, name)
                for name, text in match.groupdict().items()
                if text is not None
            )

            # Wikilink?
            if text.startswith("<a>"):
                name = match.group("a")

                if self._exists(name):
                    # Local link we have a page for
                    url_prefix, url_class = ("/help/wiki/", "Local")
                else:
                    # Wanted page where we link to the editor
                    url_prefix, url_class = (self.EDIT_URL, "Wanted")

                # Build page link
                text = '<a class="wiki-%s" href="%s%s" title="%s page %s">%s' % (
                    url_class.lower(), url_prefix, name, url_class, name, text[3:],
                )

            # Link?
            if text.startswith("<url"):
                kind = text[1:5]
                href = match.group(kind)

                # "urlb" is bracketed, "urli" is inline
                if kind == "urlb":
                    href, name = href.split(None, 1)
                else:
                    name = href

                text = u'<a href="%s" title="%s">%s</a>' % (
                    href, href, name
                )

            # Image?
            elif text.startswith("<img>"):
                text = u'<img src="%s" title="%s" />' % (
                    match.group("img"), match.group("img"),
                )

            return text

        # Call the inline replacer for each line, unless it's a code section
        self.lines = [self.RE_INLINE.sub(replacer, line)
                if not line.startswith(u"<code class") 
                else line
            for line in self.lines
        ]


    def _headings(self):
        """ Handle headings and paragraphs.
        """
        toc_line = None # number of the line containing wiki:toc
        stack = []      # section number stack
        headings = []   # list of headings found

        # Go througgh text        
        for idx, line in enumerate(self.lines):
            # If there are trailing '='...
            heading = line.rstrip('=')
            if heading is not line:
                # Caclulate heading level
                level = len(line) - len(heading)
                heading = heading.lstrip(u'=')

                # Make sure it's h1..h3 and both sides are equal length
                if 0 < level <= 3 and len(line) - len(heading) == 2 * level:
                    # Make stack the right length and increment current level
                    stack = (stack + [0]*3)[:level]
                    stack[-1] += 1

                    # Build numbered heading and put it in
                    heading = u"%s %s" % (u'.'.join(str(i) for i in stack if i), heading)
                    headings.append(heading)
                    self.lines[idx] = u"<h%d>%s</h%d>" % (level, heading, level)

            # Remember line where a TOC is requested
            if line.startswith('&lt;wiki:toc '):
                toc_line = idx

        # Want a TOC?
        if toc_line is not None:
            toc = []
            for h in headings:
                # Split up stored heading
                num, title = h.split(None, 1)
                level = num.count('.')+1

                # Build a div with 2 nested spans, so we can CSS this stuff
                toc.append(
                    u'<div><span class="wiki-toc-num-%d">%s</span>'
                    u' <span class="wiki-toc-title-%d">%s</span></div>' % (
                        level, num, level, title,
                    ))

            # Store TOC at right place
            self.lines[toc_line] = u'<div class="wiki-toc">%s</div>' % '\n'.join(toc)


    def _paragraphs(self):
        """ Handle paragraphs.
        """
        for idx, line in enumerate(self.lines):
            # Empty line that is not the first one and not after/before another empty line or HTML element?
            if (not line.strip() and 0 < idx < len(self.lines)-1 and self.lines[idx-1].strip()
                    and not self.lines[idx-1].endswith('>')
                    and not self.lines[idx+1].startswith('<h') ):
                # Use a double break so we don't need to close anything
                self.lines[idx] = u"<br /><br />"


    def _tables(self):
        """ Handle tables.
        """
        in_table = False

        for idx, line in enumerate(self.lines):
            # Is it a table line?
            if line.startswith(u"|| ") and line.endswith(u" ||"):
                # Make a row with cells
                self.lines[idx] = u"<tr><td>%s</td></tr>" % line[3:-3].replace(u"||", u"</td><td>")

                if not in_table:
                    # We just started a table
                    self.lines[idx] = u'<table>' + self.lines[idx]
                in_table = True

            elif in_table:
                # Mark end of table
                self.lines[idx-1] += u"</table>"
                in_table = False


    def _code(self):
        """ Handle code sections.
        """
        in_code = 0
        code_lines = []

        # Go thorugh all lines and assemble result in code_lines
        for line in self.lines:
            # In code section?
            if in_code:
                code_line = line.replace(u' ', u'\u00A0') + u"<br />"

                # Nested?
                if line.strip() == u"{{{":
                    in_code += 1
                    code_lines[-1] += code_line

                # End of section?
                elif line.strip() == u"}}}":
                    in_code -= 1
                    if in_code:
                        code_lines[-1] += code_line
                    else:
                        code_lines[-1] += u"</code>"

                # Add to code line
                else:
                    code_lines[-1] += code_line

            # Code section start?
            elif line.strip() == u"{{{":
                code_lines.append(u'<code class="wiki-code">')
                in_code = 1

            # Append normal line
            else:
                code_lines.append(line)

        # All code sections are now a single line, so that _inline() can ignore them
        self.lines = code_lines


    def _lists_and_rules(self):
        """ Handle lists.
        """
        stack = [(0, '')]
        for idx, line in enumerate(self.lines):
            tags = None

            # Is it an indented line?
            sline = line.lstrip()
            if sline is not line:
                indent = len(line) - len(sline)

                # Check for kind of item
                if sline.startswith("* "):
                    tags = ("ul", "li")
                elif sline.startswith("# "):
                    tags = ("ol", "li")

                # Is it an item line?
                if tags:
                    self.lines[idx] = repr((tags, sline))
                    sline = "<%s>%s</%s>" % (tags[1], sline.lstrip("*# \t"), tags[1])

                    # Indent?
                    if indent > stack[-1][0]:
                        sline = "<%s>%s" % (tags[0], sline)
                        stack.append((indent,) + tags)

                    # Dedent?
                    elif indent < stack[-1][0]:
                        sline = "</%s>%s" % (stack[-1][1], sline)
                        stack = stack[:-1]

                    # Different kind of list?
                    elif tags != stack[-1][1:]:
                        # Pop till we reached our indent level
                        while indent < stack[-1][0]:
                            sline += "</%s>" % stack[-1][1]
                            stack = stack[:-1]

                        # Close same level list of different kind, start out new list
                        sline = "</%s><%s>%s" % (stack[-1][1], tags[0], sline)
                        stack[-1] = (indent,) + tags

                    self.lines[idx] = sline

            # Horizontal rule?
            elif len(line) >= 4 and not line.strip("-"):
                self.lines[idx] = "<hr />"

            # Close all lists if not an item
            if not tags:
                while len(stack) > 1:
                    self.lines[idx-1] += "</%s>" % stack[-1][1]
                    stack = stack[:-1]


    def _parse(self):
        """ Parse the raw page text.
        """
        # Order is VERY important here!
        self.lines = [escape(line) for line in self.raw.splitlines()] + ['']
        self._metadata()
        self._code()
        self._headings()
        self._lists_and_rules()
        self._tables()
        self._paragraphs()
        self._inline()

        # Put the whole page in a wiki div
        self.lines.insert(0, '<div class="wiki">')
        self.lines.append('</div>')
        self.html = literal(u'\n'.join(self.lines))


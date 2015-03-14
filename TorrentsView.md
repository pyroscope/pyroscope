## Torrents Table ##

The info column indicates the state of each torrent: ![http://pyroscope.googlecode.com/svn/wiki/img/started.png](http://pyroscope.googlecode.com/svn/wiki/img/started.png) started / ![http://pyroscope.googlecode.com/svn/wiki/img/stopped.png](http://pyroscope.googlecode.com/svn/wiki/img/stopped.png) stopped, completion ![http://pyroscope.googlecode.com/svn/wiki/img/box-check.png](http://pyroscope.googlecode.com/svn/wiki/img/box-check.png) / ![http://pyroscope.googlecode.com/svn/wiki/img/box-cross.png](http://pyroscope.googlecode.com/svn/wiki/img/box-cross.png), active up-/download ![http://pyroscope.googlecode.com/svn/wiki/img/nuked.png](http://pyroscope.googlecode.com/svn/wiki/img/nuked.png) and tracker messages: ![http://pyroscope.googlecode.com/svn/wiki/img/info_red.png](http://pyroscope.googlecode.com/svn/wiki/img/info_red.png) severe, ![http://pyroscope.googlecode.com/svn/wiki/img/info_blue.png](http://pyroscope.googlecode.com/svn/wiki/img/info_blue.png) severe but for a closed torrent, ![http://pyroscope.googlecode.com/svn/wiki/img/info_green.png](http://pyroscope.googlecode.com/svn/wiki/img/info_green.png) informational.

The name links to the torrents detail page and has a tooltip with the most imporant data associated. The following columns show current upload / download rates, data size, transferred data volume and the upload/download ratio. The tracker column shows the domains of the announce URLs (with certain common words like "tracker" replaced by "**"), which link to a filter for that domain.**

## Filtering ##

A filter can be enabled to reduce the set of currently displayed torrents by entering patterns for  torrent names, torrent states, and tracker domains. Torrent states can be addressed by the abbreviations visible in the tooltips: OPEN, CLOSED, DONE, MSG, PRV, PUB.

Before we go into details, let's start with a few examples:
  * `*.pdf` just shows all downloaded PDF files.
  * `examp open msg` would list all the open `example.org` torrents that have a message associated with them.
  * `C` lists all torrents whose name starts with "C", and incidently, all those that are (C)losed or on a tracker domain starting with "c".
  * `c??????*` is the same as above, but won't display closed torrents (since "CLOSED" has not enough characters for that pattern).
  * `[x-z]*` matches all torrents with names at the end of the alphabet.
  * `PUB` lists all torrents with DHT/PEX enabled, while using `PRV` does the reverse.

As you can see, the filter search is a little fuzzy, but since it's meant to reduce large lists to a handy size that doesn't defeat its purpose. The main intent is to be able to pin-point data you're interested in with a few keystrokes.

The filter patterns follow the rules of shell globbing, i.e. a `*` matches any sequence of characters (including none), `?` matches exactly one character, `[seq]` matches a sequence of characters (either a list or a range like `a-z`), and finally `[!seq]` matches anything _but_ the given character set. The filtering is case-insensitive.

If you enter several patterns separated by spaces, they have to match all at once in mode AND, while selecting OR means that if any of the patterns matches a torrent, it will be displayed. Each pattern that doesn't already contain a `*` is automatically expanded to have one at the end, so that you can easily search for prefixes.
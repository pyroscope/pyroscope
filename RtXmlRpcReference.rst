Introduction
============

The following is intended to become a comprehensive reference of all the
rTorrent XMLRPC commands, a thing which is sorely missing from
rTorrent's own documentation. The information here pertains to version
0.8.6 of rTorrent, which has about 500 built-in methods.

Also see these pages for similar ressources: \* the
`RtorrentScripting <http://wiki.rtorrent.org/RtorrentScripting>`_ and
`XmlRpcReference <http://wiki.rtorrent.org/XmlRpcReference>`_ pages in
the rTorrent Community Wiki. \* the rTorrent Trac wiki has a very
incomplete `list of
commands <http://libtorrent.rakshasa.no/wiki/RTorrentCommands>`_; other
information is scattered over the other wiki pages, Trac tickets, and
the mailing list. \* `gi-torrent's draft
reference <http://code.google.com/p/gi-torrent/wiki/rTorrent_XMLRPC_reference>`_
\* `.rtorrent.rc General
Settings <http://upendo.tistory.com/entry/rtorrentrc-General-Settings>`_
is a nice blog post, limited to things you'd use in a configuration

Command syntax
==============

``command=arg1,arg2,...`` ``$`` evaluation ``"..."`` quotes ``\``
escapes ``{...}`` groups "``;``" command lists

Global commands
===============

Configuration
-------------

These commands are typically used in the ``.rtorrent.rc`` file, but many
of them are also suitable for scripting, e.g. dynamically setting the
global bandwidth throttles.

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
``import(string) ⇒ int`` \| \| Read an options file, e.g. to include
shared configuration in several instances. \| \|
``try_import(string) ⇒ int`` \| \| Like ``import``, but I/O errors are
ignored. \| \| scgi\_local(string) ⇒ int \| \| \| \| scgi\_port(string)
⇒ int \| \| \| \| get\_xmlrpc\_size\_limit() ⇒ int
set\_xmlrpc\_size\_limit(int) ⇒ int \| 524288 \| The maximum XMLRPC
payload size. \| \| xmlrpc\_dialect(string) ⇒ int \| \| Set the XMLRPC
dialect to use (*details ==> source code*) \| \| system.set\_umask(int)
⇒ int \| \| \| \| \| \| **TODO** \|

System information
------------------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| get\_ip() ⇒
string set\_ip(string) ⇒ int \| '0.0.0.0' \| \| \| get\_key\_layout() ⇒
string set\_key\_layout(string) ⇒ int \| 'qwerty' \| Current keyboard
layout. \| \| system.pid() ⇒ int \| 11848 \| Process ID. \| \|
system.time() ⇒ int \| 1282251105 \| Current time in seconds since
1970-01-01. \| \| system.time\_seconds() ⇒ int \| 1282251105 \| Current
time in seconds since 1970-01-01. \| \| system.time\_usec() ⇒ long \|
1282251105786209L \| Current time in µs since 1970-01-01. \| \|
system.client\_version() ⇒ string \| '0.8.6' \| rTorrent version. \| \|
system.library\_version() ⇒ string \| '0.12.6' \| libtorrent version. \|
\| system.get\_cwd() ⇒ string system.set\_cwd(string path) ⇒ int \|
'~/lib/rtorrent' \| Current working directory, \| \| system.hostname() ⇒
string \| 'example' \| System's hostname. \| \| system.capabilities() ⇒
struct \| {'facility': 'xmlrpc-c', 'protocol\_version': 2,
'version\_major': 1, 'version\_minor': 21, 'version\_point': 2} \|
Return the capabilities of this XML-RPC server. \| \|
system.getCapabilities() ⇒ struct \| {'introspect': {'specUrl':
'http://xmlrpc-c.....html', 'specVersion': 1}} \| Return the list of
standard capabilities of this XML-RPC server. See
http://tech.groups.yahoo.com/group/xml-rpc/message/2897. \| \|
system.listMethods() ⇒ array \| ``['system.listMethods',`` ...``]`` \|
Return an array of all available XML-RPC methods on this server. \| \|
system.methodExist(string name) ⇒ boolean \| ``True`` (called on itself)
\| Tell whether a method by a specified name exists on this server. \|
\| system.methodHelp(string) ⇒ string \| \| Given the name of a method,
return a help string. \| \| system.methodSignature(string) ⇒ array \| \|
Given the name of a method, return an array of legal signatures. Each
signature is an array of strings. The first item of each signature is
the return type, and any others items are parameter types. \| \|
system.multicall(array) ⇒ array \| \| Process an array of calls, and
return an array of results. Calls should be structs of the form
``{'methodName': string, 'params': array}``. Each result will either be
a single-item array containg the result value, or a struct of the form
``{'faultCode': int, 'faultString': string}``. This is useful when you
need to make lots of small calls without lots of round trips. \| \| \|
\| **TODO** \|

Logging and formatting
----------------------

**NOTE:** The conversion functions take either strings or longs.

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| print(string arg,
...) ⇒ int \| \| Dump the string arguments into the log. \| \| cat(arg)
⇒ string \| \| Convert ``arg`` to string. \| \| to\_date(int) ⇒ string
\| ``1282398703`` ⇒ ``'21/08/2010'`` \| Convert UNIX localtime to date
string. \| \| to\_time(int) ⇒ string \| ``1282398703`` ⇒ ``'15:51:43'``
\| Convert UNIX localtime to time string. \| \| to\_elapsed\_time(int) ⇒
string \| ``' 0:02:11'`` \| Time delta between UNIX timestamp and now.
\| \| to\_gm\_date(int) ⇒ string \| ``1282398703`` ⇒ ``'21/08/2010'`` \|
Convert UNIX UTC time to date string. \| \| to\_gm\_time(int) ⇒ string
\| ``1282398703`` ⇒ ``'13:51:43'`` \| Convert UNIX UTC time to time
string. \| \| to\_kb(int) ⇒ string \| -1024 ⇒ ``' -1,0'`` \| Convert
bytes to ``KiB`` (length 5). \| \| to\_mb(int) ⇒ string \| 2000000 ⇒
``'     1,9'`` \| Convert bytes to ``MiB`` (length 8). \| \| to\_xb(int)
⇒ string \| 4000000000 ⇒ ``'  3,7 GB'`` \| Convert bytes to auto-scaled
value (length 8). \| \| to\_throttle(int) ⇒ string \| 65535 ⇒ ``' 63'``
\| Convert bytes to ``KiB`` (length 3). \|

Events
======

State changes
-------------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
close\_low\_diskspace(**TODO**) ⇒ int \| \| **TODO** \| \| \| \|
**TODO** \| \| event.download.closed() ⇒ undef \| \| **TODO** \| \|
event.download.erased() ⇒ undef \| \| **TODO** \| \|
event.download.finished() ⇒ undef \| \| **TODO** \| \|
event.download.hash\_done() ⇒ undef \| \| **TODO** \| \|
event.download.hash\_queued() ⇒ undef \| \| **TODO** \| \|
event.download.hash\_removed() ⇒ undef \| \| **TODO** \| \|
event.download.inserted() ⇒ undef \| \| **TODO** \| \|
event.download.inserted\_new() ⇒ undef \| \| **TODO** \| \|
event.download.inserted\_session() ⇒ undef \| \| **TODO** \| \|
event.download.opened() ⇒ undef \| \| **TODO** \| \|
event.download.paused() ⇒ undef \| \| **TODO** \| \|
event.download.resumed() ⇒ undef \| \| **TODO** \|

Scheduling
----------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| schedule() ⇒ int
\| \| **TODO** \| \| schedule\_remove(string) ⇒ int \| \| **TODO** \| \|
scheduler.max\_active() ⇒ undef \| \| **TODO** \| \|
scheduler.max\_active.set() ⇒ undef \| \| **TODO** \| \|
scheduler.simple.added() ⇒ int \| \| **TODO** \| \|
scheduler.simple.removed() ⇒ int \| \| **TODO** \| \|
scheduler.simple.update() ⇒ int \| \| **TODO** \|

Control flow
============

Conditions
----------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| false() ⇒ int \|
\| **TODO** \| \| or() ⇒ int \| \| **TODO** \| \| and() ⇒ int \| \|
**TODO** \| \| not() ⇒ int \| \| **TODO** \| \| less(int) ⇒ int \| \|
**TODO** \| \| greater(int) ⇒ int \| \| **TODO** \| \| equal \| \| *SVN
head only?!* **TODO** \| \| \| \| **TODO** \|

Conditional execution
---------------------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| branch() ⇒ int \|
\| **TODO** \| \| if() ⇒ int \| \| **TODO** \| \| \| \| **TODO** \|

Macros (user-defined commands)
------------------------------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
system.method.erase() ⇒ int \| \| **TODO** \| \| system.method.get() ⇒
int \| \| **TODO** \| \| system.method.has\_key() ⇒ int \| \| **TODO**
\| \| system.method.insert() ⇒ int \| \| **TODO** \| \|
system.method.list\_keys() ⇒ int \| \| **TODO** \| \|
system.method.set() ⇒ int \| \| **TODO** \| \| system.method.set\_key()
⇒ int \| \| **TODO** \| \| argument.0() ⇒ any \| \| **TODO** \| \|
argument.1() ⇒ any \| \| **TODO** \| \| argument.2() ⇒ any \| \|
**TODO** \| \| argument.3() ⇒ any \| \| **TODO** \|

Download items
==============

Attributes
----------

**NOTE:** All the calls working on download items take the hash of the
item as their first parameter. The following table omits this parameter,
and in multicalls you have to actually leave it out since it's provided
by the system.

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
d.multicall(string view, commands...) ⇒ 2-dim array \|
``[['00...C8', 0],`` ...``]]`` \| Call a set of ``d.`` commands on all
items in a view, e.g.
``rtxmlrpc d.multicall main d.get_hash= d.get_up_rate=``. \| \|
d.get\_hash() ⇒ string \| ``'00...C8'`` \| The info hash. \| \|
d.get\_ratio() ⇒ int \| ``1000`` \| Ratio [‰]. \| \|
d.get\_base\_filename() ⇒ string \| ``'base'`` \| File or root directory
name of torrent. \| \| d.get\_base\_path() ⇒ string \| ``'/dir/base'``
\| Path to download directory or file. \| \| d.get\_directory() ⇒ string
\| ``'/dir'`` or ``'/dir/multi'`` \| Path containing the download \| \|
d.get\_directory\_base() ⇒ string \| ``'/dir'`` or ``'/dir/multi'`` \|
**Difference to d.get\_directory?** \| \| d.get\_loaded\_file() ⇒ string
\| ``'.../.session/00...C8.torrent'`` \| Path to the session file. \| \|
d.get\_size\_bytes() ⇒ int \| ``123456`` \| Exact total size in bytes.
\| \| d.get\_size\_chunks() ⇒ int \| ``4`` \| Total size in chunks. \|
\| d.get\_message() ⇒ string d.set\_message(string) ⇒ int \|
``'Tracker: [Tried all trackers.]'`` \| Current (tracker) message. \| \|
d.get\_custom(string key) ⇒ string d.get\_custom\_throw(string key) ⇒
string d.set\_custom(string key, string val) ⇒ int \| \| Get and set
arbitrary amounts of custom attributes. The ``throw`` variant returns a
``<Fault -503: 'No such custom value.'>`` for unknown keys, else an
empty string is returned as a default. \| \| d.get\_custom1() ⇒ string
d.set\_custom1(string val) ⇒ int (and 2, 3, 4, 5) \| \| Get and set up
to 5 custom values. **TODO: Document what these are typically used for,
there is a de-facto standard.** \|

\| d.get\_bitfield() ⇒ int \| \| **TODO** \|
\|:--------------------------\|:-\|:----------\| \| d.get\_bytes\_done()
⇒ int \| \| **TODO** \| \| d.get\_chunk\_size() ⇒ int \| \| **TODO** \|
\| d.get\_chunks\_hashed() ⇒ int \| \| **TODO** \| \| d.get\_complete()
⇒ int \| \| **TODO** \| \| d.get\_completed\_bytes() ⇒ int \| \|
**TODO** \| \| d.get\_completed\_chunks() ⇒ int \| \| **TODO** \| \|
d.get\_connection\_current() ⇒ string \| \| **TODO** \| \|
d.get\_connection\_leech() ⇒ int \| \| **TODO** \| \|
d.get\_connection\_seed() ⇒ int \| \| **TODO** \| \|
d.get\_creation\_date() ⇒ int \| \| **TODO** \| \| d.get\_down\_rate() ⇒
int \| \| **TODO** \| \| d.get\_down\_total() ⇒ int \| \| **TODO** \| \|
d.get\_free\_diskspace() ⇒ int \| \| **TODO** \| \| d.get\_hashing() ⇒
int \| \| **TODO** \| \| d.get\_hashing\_failed() ⇒ int \| \| **TODO**
\| \| d.get\_ignore\_commands() ⇒ int \| \| **TODO** \| \|
d.get\_left\_bytes() ⇒ int \| \| **TODO** \| \| d.get\_local\_id() ⇒ int
\| \| **TODO** \| \| d.get\_local\_id\_html() ⇒ int \| \| **TODO** \| \|
d.get\_max\_file\_size() ⇒ int \| \| **TODO** \| \|
d.get\_max\_size\_pex() ⇒ int \| \| **TODO** \| \| d.get\_mode() ⇒ int
\| \| **TODO** \| \| d.get\_name() ⇒ string \| \| **TODO** \| \|
d.get\_peer\_exchange() ⇒ int \| \| **TODO** \| \|
d.set\_peer\_exchange(int) ⇒ int \| \| **TODO** \| \|
d.get\_peers\_accounted() ⇒ int \| \| **TODO** \| \|
d.get\_peers\_complete() ⇒ int \| \| **TODO** \| \|
d.get\_peers\_connected() ⇒ int \| \| **TODO** \| \| d.get\_peers\_max()
⇒ int \| \| **TODO** \| \| d.set\_peers\_max(int) ⇒ int \| \| **TODO**
\| \| d.get\_peers\_min() ⇒ int \| \| **TODO** \| \|
d.set\_peers\_min(int) ⇒ int \| \| **TODO** \| \|
d.get\_peers\_not\_connected() ⇒ int \| \| **TODO** \| \|
d.get\_priority() ⇒ int \| \| **TODO** \| \| d.set\_priority(int) ⇒ int
\| \| **TODO** \| \| d.get\_priority\_str() ⇒ string \| \| **TODO** \|
\| d.get\_size\_pex() ⇒ int \| \| **TODO** \| \| d.get\_skip\_rate() ⇒
int \| \| **TODO** \| \| d.get\_skip\_total() ⇒ int \| \| **TODO** \| \|
d.get\_state() ⇒ int \| \| **TODO** \| \| d.get\_state\_changed() ⇒ int
\| \| **TODO** \| \| d.get\_state\_counter() ⇒ int \| \| **TODO** \| \|
d.get\_throttle\_name() ⇒ int \| \| **TODO** \| \|
d.get\_tied\_to\_file() ⇒ int \| \| **TODO** \| \|
d.get\_tracker\_focus() ⇒ int \| \| **TODO** \| \|
d.get\_tracker\_numwant() ⇒ int \| \| **TODO** \| \|
d.get\_tracker\_size() ⇒ int \| \| **TODO** \| \| d.get\_up\_rate() ⇒
int \| \| **TODO** \| \| d.get\_up\_total() ⇒ int \| \| **TODO** \| \|
d.get\_uploads\_max() ⇒ int \| \| **TODO** \| \| d.is\_active() ⇒ int \|
\| **TODO** \| \| d.is\_hash\_checked() ⇒ int \| \| **TODO** \| \|
d.is\_hash\_checking() ⇒ int \| \| **TODO** \| \| d.is\_multi\_file() ⇒
int \| \| **TODO** \| \| d.is\_open() ⇒ int \| \| **TODO** \| \|
d.is\_pex\_active() ⇒ int \| \| **TODO** \| \| d.is\_private() ⇒ int \|
\| **TODO** \| \| d.set\_connection\_current(string) ⇒ int \| \|
**TODO** \| \| d.set\_directory(string) ⇒ int \| \| **TODO** \| \|
d.set\_directory\_base(string) ⇒ int \| \| **TODO** \| \|
d.set\_hashing\_failed(int) ⇒ int \| \| **TODO** \| \|
d.set\_ignore\_commands(int) ⇒ int \| \| **TODO** \| \|
d.set\_max\_file\_size(int) ⇒ int \| \| **TODO** \| \|
d.set\_throttle\_name(string) ⇒ int \| \| **TODO** \| \|
d.set\_tied\_to\_file(string) ⇒ int \| \| **TODO** \| \|
d.set\_tracker\_numwant(int) ⇒ int \| \| **TODO** \| \|
d.set\_uploads\_max(int) ⇒ int \| \| **TODO** \| \|
d.update\_priorities() ⇒ int \| \| **TODO** \| \| d.views() ⇒ int \| \|
**TODO** \| \| d.views.has() ⇒ int \| \| **TODO** \| \|
d.views.push\_back() ⇒ int \| \| **TODO** \| \|
d.views.push\_back\_unique() ⇒ int \| \| **TODO** \| \| d.views.remove()
⇒ int \| \| **TODO** \|

Files
-----

**NOTE:** You need to call the file related methods with the info hash
and the zero-based file index as the first two arguments.

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
d.get\_size\_files() ⇒ int \| \| Number of files in item. This returns 1
for single-file torrents. \| \| f.multicall(method=, ...) ⇒ array \| \|
Call several file-related methods at once on all the files in an item,
e.g.
"``rtxmlrpc f.multicall 00...C8 +0 f.get_size_bytes= f.get_path=``". \|
\| f.get\_path() ⇒ string \| ``'a/b'`` \| Relative path as a string. \|
\| f.get\_path\_components() ⇒ array of string \| ``['a', 'b']`` \|
Relative path as an array. \| \| f.get\_path\_depth() ⇒ int \| ``'2'``
\| Number of path components. \| \| f.get\_frozen\_path() ⇒ string \|
``'/dir/base/a/b'`` \| Full path to the file. \| \| f.is\_created() ⇒
int \| ``0`` or ``1`` \| File created? \| \| f.is\_open() ⇒ int \| ``0``
or ``1`` \| File opened? \| \| f.get\_size\_bytes() ⇒ int \| ``2760726``
\| Exact size in bytes. \| \| f.get\_size\_chunks() ⇒ int \| ``6`` \|
Size in chunks. \| \| f.get\_last\_touched() ⇒ int \|
``1282422238906187`` \| File modification date (UNIX timestamp). **TODO:
...or something else, maybe the last time rT checked the file** \| \|
f.get\_priority() ⇒ int f.set\_priority(int) ⇒ int \| ``1`` \| Priority
(0=off, 1=normal, 2=high) \| \| f.get\_completed\_chunks() ⇒ int \|
``6`` \| Number of chunks already completed. \| \|
f.get\_match\_depth\_next() ⇒ int \| \| **TODO** \| \|
f.get\_match\_depth\_prev() ⇒ int \| \| **TODO** \| \| f.get\_offset() ⇒
int \| \| **TODO** \| \| f.get\_range\_first() ⇒ int \| \| **TODO** \|
\| f.get\_range\_second() ⇒ int \| \| **TODO** \| \|
f.is\_create\_queued() ⇒ int f.set\_create\_queued() ⇒ int
f.unset\_create\_queued() ⇒ int \| \| **TODO** \| \|
f.is\_resize\_queued() ⇒ int f.set\_resize\_queued() ⇒ int
f.unset\_resize\_queued() ⇒ int \| \| **TODO** \|

Trackers
--------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| t.multicall() ⇒
int \| \| **TODO** \| \| \| \| **TODO** \| \| t.get\_group() ⇒ int \| \|
**TODO** \| \| t.get\_id() ⇒ string \| \| **TODO** \| \|
t.get\_min\_interval() ⇒ int \| \| **TODO** \| \|
t.get\_normal\_interval() ⇒ int \| \| **TODO** \| \|
t.get\_scrape\_complete() ⇒ int \| \| **TODO** \| \|
t.get\_scrape\_downloaded() ⇒ int \| \| **TODO** \| \|
t.get\_scrape\_incomplete() ⇒ int \| \| **TODO** \| \|
t.get\_scrape\_time\_last() ⇒ int \| \| **TODO** \| \| t.get\_type() ⇒
int \| \| **TODO** \| \| t.get\_url() ⇒ string \| \| **TODO** \| \|
t.is\_enabled() ⇒ int \| \| **TODO** \| \| t.is\_open() ⇒ int \| \|
**TODO** \| \| t.set\_enabled(int) ⇒ int \| \| **TODO** \|

Peers
-----

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
d.add\_peer(string) ⇒ int \| \| **TODO** \| \| p.multicall() ⇒ int \| \|
**TODO** \| \| \| \| **TODO** \| \| p.get\_address() ⇒ string \| \|
**TODO** \| \| p.get\_client\_version() ⇒ string \| \| **TODO** \| \|
p.get\_completed\_percent() ⇒ int \| \| **TODO** \| \|
p.get\_down\_rate() ⇒ int \| \| **TODO** \| \| p.get\_down\_total() ⇒
int \| \| **TODO** \| \| p.get\_id() ⇒ string \| \| **TODO** \| \|
p.get\_id\_html() ⇒ string \| \| **TODO** \| \| p.get\_options\_str() ⇒
string \| \| **TODO** \| \| p.get\_peer\_rate() ⇒ int \| \| **TODO** \|
\| p.get\_peer\_total() ⇒ int \| \| **TODO** \| \| p.get\_port() ⇒ int
\| \| **TODO** \| \| p.get\_up\_rate() ⇒ int \| \| **TODO** \| \|
p.get\_up\_total() ⇒ int \| \| **TODO** \| \| p.is\_encrypted() ⇒ int \|
\| **TODO** \| \| p.is\_incoming() ⇒ int \| \| **TODO** \| \|
p.is\_obfuscated() ⇒ int \| \| **TODO** \| \| p.is\_snubbed() ⇒ int \|
\| **TODO** \|

Management
----------

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| \| \| **TODO** \|
\| d.start() ⇒ undef \| \| **TODO** \| \| d.stop() ⇒ undef \| \|
**TODO** \| \| d.try\_close() ⇒ undef \| \| **TODO** \| \|
d.try\_start() ⇒ undef \| \| **TODO** \| \| d.try\_stop() ⇒ undef \| \|
**TODO** \| \| d.check\_hash() ⇒ int \| \| **TODO** \| \| d.close() ⇒
int \| \| **TODO** \| \| d.erase() ⇒ int \| \| **TODO** \| \| d.open() ⇒
int \| \| **TODO** \| \| d.pause() ⇒ int \| \| **TODO** \| \| d.resume()
⇒ int \| \| **TODO** \| \| d.save\_session() ⇒ int \| \| **TODO** \| \|
d.create\_link() ⇒ int \| \| **TODO** \| \| d.delete\_link() ⇒ int \| \|
**TODO** \| \| d.delete\_tied() ⇒ int \| \| **TODO** \| \|
d.initialize\_logs() ⇒ int \| \| **TODO** \|

Views
=====

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
ui.current\_view.set(string name) ⇒ int \| \| Change currently visible
view. \| \| view\_list() ⇒ array \| ``['main',`` ...``,`` ``'seeding']``
\| Return all currently defined views. \| \| view\_add(string) ⇒ int \|
\| Add a *new* view. **Do NOT try to add an already defined view!** \|
\| view\_sort(string view) ⇒ int \| \| Sort again in the defined order.
\| \| view\_sort\_current(string view, string comparator) ⇒ int \| \|
Sort current view content now. \| \| view\_sort\_new(string view, string
comparator) ⇒ int \| \| Define sort order for newly added items. \| \|
view\_filter(string view, string condition) ⇒ int \| \| Filter items by
condition once. Use a schedule or events to keep it up to date. \| \|
view\_filter\_on(string view, string event) ⇒ int \| \| Sort again on
event. **OR EVENT LIST?! ARRAY? MULTI-ARG?** \| \|
``view.set_visible(infohash, viewname) ⇒ int``
``view.set_not_visible(infohash, viewname) ⇒ int`` \| \| Add or remove
single item. \| \| \| \| **TODO** \| \| view.event\_added() ⇒ int \| \|
**TODO** \| \| view.event\_removed() ⇒ int \| \| **TODO** \| \|
view.filter\_download() ⇒ int \| \| **TODO** \| \| view.persistent() ⇒
int \| \| **TODO** \| \| view.size() ⇒ int \| \| **TODO** \| \|
view.size\_not\_visible() ⇒ int \| \| **TODO** \| \| view\_set() ⇒ array
\| \| **TODO** \|

Some handy commands: \* To clear a view, use
``view_filter=NAME,false=``. \* To make a view visible, execute
``ui.current_view.set=NAME``.

Ratio management
================

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| \| \| **TODO** \|
\| ratio.disable() ⇒ undef \| \| **TODO** \| \| ratio.enable() ⇒ undef
\| \| **TODO** \| \| ratio.max() ⇒ undef \| \| **TODO** \| \|
ratio.max.set() ⇒ undef \| \| **TODO** \| \| ratio.min() ⇒ undef \| \|
**TODO** \| \| ratio.min.set() ⇒ undef \| \| **TODO** \| \|
ratio.upload() ⇒ undef \| \| **TODO** \| \| ratio.upload.set() ⇒ undef
\| \| **TODO** \|

Bandwidth management
====================

Throttles work by sharing from the global bandwidth limits, i.e. those
have to be set for throttles to actually work. You can set the global
limits to values higher than your actually available bandwidth if you
want "unlimited".

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
throttle\_down(string name, string limit) ⇒ int \| \| Create or reset a
download throttle. The limit is a string and in ``KiB``. \| \|
throttle\_up(string name, string limit) ⇒ int \| \| Create or reset an
upload throttle. The limit is a string and in ``KiB``. \| \|
throttle\_ip(**TODO**) ⇒ int \| \| **TODO** \| \| \| \| **TODO** \|

Miscellaneous
=============

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \|
system.shutdown(string ???) ⇒ int \| 0 \| Shut down the server. Return
code is always zero. \| \| session\_save() ⇒ int \| \| Save session data
for all items right now. \| \| \| \| **TODO** \|

Unsorted material
=================

This is what introspection on the rTorrent interfaces returns — a lot of
this information, especially the signatures and return types, are
probably not 100% correct.

C \| call\_download() ⇒ int \| \| **TODO** \|
\|:-------------------------\|:-\|:----------\| \| close\_untied() ⇒ int
\| \| **TODO** \| \| create\_link() ⇒ int \| \| **TODO** \|

D \| delete\_link() ⇒ int \| \| **TODO** \|
\|:-----------------------\|:-\|:----------\| \| dht(string) ⇒ int \| \|
**TODO** \| \| dht\_add\_node(string) ⇒ int \| \| **TODO** \| \|
dht\_statistics() ⇒ struct \| {'active': 0, 'dht': 'disable',
'throttle': ''} \| **TODO** \| \| download\_list() ⇒ int \| \| **TODO**
\|

E \| enable\_trackers(int) ⇒ int \| \| **TODO** \|
\|:------------------------------\|:-\|:----------\| \|
encoding\_list(string) ⇒ int \| \| **TODO** \| \| encryption() ⇒ int \|
\| **TODO** \| \| execute() ⇒ int \| \| **TODO** \| \|
execute\_capture() ⇒ int \| \| **TODO** \| \|
execute\_capture\_nothrow() ⇒ int \| \| **TODO** \| \|
execute\_nothrow() ⇒ int \| \| **TODO** \| \| execute\_raw() ⇒ int \| \|
**TODO** \| \| execute\_raw\_nothrow() ⇒ int \| \| **TODO** \|

F \| fi.get\_filename\_last() ⇒ int \| \| **TODO** \|
\|:---------------------------------\|:-\|:----------\| \| fi.is\_file()
⇒ int \| \| **TODO** \|

G \| get\_bind() ⇒ string '0.0.0.0' \| \| **TODO** \|
\|:----------------------------------------------\|:-\|:----------\| \|
get\_check\_hash() ⇒ int 1 \| \| **TODO** \| \| get\_connection\_leech()
⇒ int 'leech' \| \| **TODO** \| \| get\_connection\_seed() ⇒ int 'seed'
\| \| **TODO** \| \| get\_dht\_port() ⇒ int 6881 \| \| **TODO** \| \|
get\_dht\_throttle() ⇒ string \| \| **TODO** \| \| get\_directory() ⇒
int '~/lib/rtorrent/work' \| \| **TODO** \| \| get\_down\_rate() ⇒ int
306 \| \| **TODO** \| \| get\_down\_total() ⇒ int 4718667514L \| \|
**TODO** \| \| get\_download\_rate() ⇒ int 634880 \| \| **TODO** \| \|
get\_handshake\_log() ⇒ int \| \| **TODO** \| \| get\_hash\_interval() ⇒
int \| \| **TODO** \| \| get\_hash\_max\_tries() ⇒ int \| \| **TODO** \|
\| get\_hash\_read\_ahead() ⇒ int \| \| **TODO** \| \|
get\_http\_cacert() ⇒ string \| \| **TODO** \| \| get\_http\_capath() ⇒
string \| \| **TODO** \| \| get\_http\_proxy() ⇒ string \| \| **TODO**
\| \| get\_log.tracker() ⇒ int \| \| **TODO** \| \|
get\_max\_downloads\_div() ⇒ int 1 \| \| **TODO** \| \|
get\_max\_downloads\_global() ⇒ int 50 \| \| **TODO** \| \|
get\_max\_file\_size() ⇒ int -1 \| \| **TODO** \| \|
get\_max\_memory\_usage() ⇒ int 858993459 \| \| **TODO** \| \|
get\_max\_open\_files() ⇒ int 128 \| \| **TODO** \| \|
get\_max\_open\_http() ⇒ int 32 \| \| **TODO** \| \|
get\_max\_open\_sockets() ⇒ int 300 \| \| **TODO** \| \|
get\_max\_peers() ⇒ int 40 \| \| **TODO** \| \| get\_max\_peers\_seed()
⇒ int 30 \| \| **TODO** \| \| get\_max\_uploads() ⇒ int 15 \| \|
**TODO** \| \| get\_max\_uploads\_div() ⇒ int 1 \| \| **TODO** \| \|
get\_max\_uploads\_global() ⇒ int 10 \| \| **TODO** \| \|
get\_memory\_usage() ⇒ int 786432 \| \| **TODO** \| \| get\_min\_peers()
⇒ int 40 \| \| **TODO** \| \| get\_min\_peers\_seed() ⇒ int -1 \| \|
**TODO** \| \| get\_name() ⇒ int 'example:11848' \| \| **TODO** \| \|
get\_peer\_exchange() ⇒ int 0 \| \| **TODO** \| \| get\_port\_open() ⇒
int 1 \| \| **TODO** \| \| get\_port\_random() ⇒ int 0 \| \| **TODO** \|
\| get\_port\_range() ⇒ int '54300-54399' \| \| **TODO** \| \|
get\_preload\_min\_size() ⇒ int \| \| **TODO** \| \|
get\_preload\_required\_rate() ⇒ int \| \| **TODO** \| \|
get\_preload\_type() ⇒ int \| \| **TODO** \| \| get\_proxy\_address() ⇒
string \| \| **TODO** \| \| get\_receive\_buffer\_size() ⇒ int \| \|
**TODO** \| \| get\_safe\_free\_diskspace() ⇒ int 537657344 \| \|
**TODO** \| \| get\_safe\_sync() ⇒ int \| \| **TODO** \| \|
get\_scgi\_dont\_route() ⇒ int \| \| **TODO** \| \|
get\_send\_buffer\_size() ⇒ int 0 \| \| **TODO** \| \| get\_session() ⇒
string '~/lib/rtorrent/.session/' \| \| **TODO** \| \|
get\_session\_lock() ⇒ int 1 \| \| **TODO** \| \|
get\_session\_on\_completion() ⇒ int \| \| **TODO** \| \|
get\_split\_file\_size() ⇒ int \| \| **TODO** \| \| get\_split\_suffix()
⇒ int \| \| **TODO** \| \| get\_stats\_not\_preloaded() ⇒ int 81787 \|
\| **TODO** \| \| get\_stats\_preloaded() ⇒ int 0 \| \| **TODO** \| \|
get\_throttle\_down\_max(string) ⇒ int \| \| **TODO** \| \|
get\_throttle\_down\_rate(string) ⇒ int \| \| **TODO** \| \|
get\_throttle\_up\_max(string) ⇒ int \| \| **TODO** \| \|
get\_throttle\_up\_rate(string) ⇒ int \| \| **TODO** \| \|
get\_timeout\_safe\_sync() ⇒ int \| \| **TODO** \| \|
get\_timeout\_sync() ⇒ int \| \| **TODO** \| \| get\_tracker\_numwant()
⇒ int \| \| **TODO** \| \| get\_up\_rate() ⇒ int 61111 \| \| **TODO** \|
\| get\_up\_total() ⇒ int 6535528158L \| \| **TODO** \| \|
get\_upload\_rate() ⇒ int 63488 \| \| **TODO** \| \|
get\_use\_udp\_trackers() ⇒ int 0 \| \| **TODO** \|

\| group.insert() ⇒ int \| \| **TODO** \|
\|:-----------------------\|:-\|:----------\| \|
group.insert\_persistent\_view() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.command() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.disable() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.enable() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.max() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.max.set() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.min() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.min.set() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.upload() ⇒ undef \| \| **TODO** \| \|
group.seeding.ratio.upload.set() ⇒ undef \| \| **TODO** \| \|
group.seeding.view() ⇒ undef \| \| **TODO** \| \|
group.seeding.view.set() ⇒ undef \| \| **TODO** \|

L \| load() ⇒ int \| \| **TODO** \|
\|:---------------\|:-\|:----------\| \| load\_raw() ⇒ int \| \|
**TODO** \| \| load\_raw\_start() ⇒ int \| \| **TODO** \| \|
load\_raw\_verbose() ⇒ int \| \| **TODO** \| \| load\_start() ⇒ int \|
\| **TODO** \| \| load\_start\_verbose() ⇒ int \| \| **TODO** \| \|
load\_verbose() ⇒ int \| \| **TODO** \| \| log.execute(string) ⇒ int \|
\| **TODO** \| \| log.xmlrpc(string) ⇒ int \| \| **TODO** \|

O \| on\_close() ⇒ int \| \| **TODO** \|
\|:--------------------\|:-\|:----------\| \| on\_erase() ⇒ int \| \|
**TODO** \| \| on\_finished() ⇒ int \| \| **TODO** \| \|
on\_hash\_queued() ⇒ int \| \| **TODO** \| \| on\_hash\_removed() ⇒ int
\| \| **TODO** \| \| on\_insert() ⇒ int \| \| **TODO** \| \| on\_open()
⇒ int \| \| **TODO** \| \| on\_ratio(string) ⇒ int \| \| **TODO** \| \|
on\_start() ⇒ int \| \| **TODO** \| \| on\_stop() ⇒ int \| \| **TODO**
\|

R \| remove\_untied() ⇒ int \| \| **TODO** \|
\|:-------------------------\|:-\|:----------\|

S \| set\_bind(string) ⇒ int \| \| **TODO** \|
\|:--------------------------\|:-\|:----------\| \| set\_check\_hash() ⇒
int \| \| **TODO** \| \| set\_connection\_leech() ⇒ int \| \| **TODO**
\| \| set\_connection\_seed() ⇒ int \| \| **TODO** \| \|
set\_dht\_port() ⇒ int \| \| **TODO** \| \| set\_dht\_throttle(string) ⇒
int \| \| **TODO** \| \| set\_directory() ⇒ int \| \| **TODO** \| \|
set\_download\_rate(int) ⇒ int \| \| **TODO** \| \|
set\_handshake\_log() ⇒ int \| \| **TODO** \| \|
set\_hash\_interval(int) ⇒ int \| \| **TODO** \| \|
set\_hash\_max\_tries(int) ⇒ int \| \| **TODO** \| \|
set\_hash\_read\_ahead(int) ⇒ int \| \| **TODO** \| \|
set\_http\_cacert(string) ⇒ int \| \| **TODO** \| \|
set\_http\_capath(string) ⇒ int \| \| **TODO** \| \|
set\_http\_proxy(string) ⇒ int \| \| **TODO** \| \| set\_log.tracker() ⇒
int \| \| **TODO** \| \| set\_max\_downloads\_div() ⇒ int \| \| **TODO**
\| \| set\_max\_downloads\_global() ⇒ int \| \| **TODO** \| \|
set\_max\_file\_size() ⇒ int \| \| **TODO** \| \|
set\_max\_memory\_usage(int) ⇒ int \| \| **TODO** \| \|
set\_max\_open\_files(int) ⇒ int \| \| **TODO** \| \|
set\_max\_open\_http(int) ⇒ int \| \| **TODO** \| \|
set\_max\_open\_sockets(int) ⇒ int \| \| **TODO** \| \|
set\_max\_peers() ⇒ int \| \| **TODO** \| \| set\_max\_peers\_seed() ⇒
int \| \| **TODO** \| \| set\_max\_uploads() ⇒ int \| \| **TODO** \| \|
set\_max\_uploads\_div() ⇒ int \| \| **TODO** \| \|
set\_max\_uploads\_global() ⇒ int \| \| **TODO** \| \| set\_min\_peers()
⇒ int \| \| **TODO** \| \| set\_min\_peers\_seed() ⇒ int \| \| **TODO**
\| \| set\_name() ⇒ int \| \| **TODO** \| \| set\_peer\_exchange() ⇒ int
\| \| **TODO** \| \| set\_port\_open() ⇒ int \| \| **TODO** \| \|
set\_port\_random() ⇒ int \| \| **TODO** \| \| set\_port\_range() ⇒ int
\| \| **TODO** \| \| set\_preload\_min\_size(int) ⇒ int \| \| **TODO**
\| \| set\_preload\_required\_rate(int) ⇒ int \| \| **TODO** \| \|
set\_preload\_type(int) ⇒ int \| \| **TODO** \| \|
set\_proxy\_address(string) ⇒ int \| \| **TODO** \| \|
set\_receive\_buffer\_size(int) ⇒ int \| \| **TODO** \| \|
set\_safe\_sync(int) ⇒ int \| \| **TODO** \| \| set\_scgi\_dont\_route()
⇒ int \| \| **TODO** \| \| set\_send\_buffer\_size(int) ⇒ int \| \|
**TODO** \| \| set\_session(string) ⇒ int \| \| **TODO** \| \|
set\_session\_lock() ⇒ int \| \| **TODO** \| \|
set\_session\_on\_completion() ⇒ int \| \| **TODO** \| \|
set\_split\_file\_size() ⇒ int \| \| **TODO** \| \| set\_split\_suffix()
⇒ int \| \| **TODO** \| \| set\_timeout\_safe\_sync(int) ⇒ int \| \|
**TODO** \| \| set\_timeout\_sync(int) ⇒ int \| \| **TODO** \| \|
set\_tracker\_numwant() ⇒ int \| \| **TODO** \| \|
set\_upload\_rate(int) ⇒ int \| \| **TODO** \| \|
set\_use\_udp\_trackers() ⇒ int \| \| **TODO** \| \| start\_tied() ⇒ int
\| \| **TODO** \| \| stop\_untied() ⇒ int \| \| **TODO** \| \|
system.file\_allocate() ⇒ undef \| \| **TODO** \| \|
system.file\_allocate.set() ⇒ undef \| \| **TODO** \| \|
system.file\_status\_cache.prune() ⇒ int \| \| **TODO** \| \|
system.file\_status\_cache.size() ⇒ int \| \| **TODO** \|

T \| tos(string) ⇒ int \| \| **TODO** \|
\|:--------------------\|:-\|:----------\|

U \| ui.unfocus\_download() ⇒ int \| \| **TODO** \|
\|:-------------------------------\|:-\|:----------\|

\| **Command** \| **Example** \| **Description** \|
\|:------------\|:------------\|:----------------\| \| \| \| **TODO** \|

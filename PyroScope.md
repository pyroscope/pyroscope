

# Introduction #

PyroScope is a collection of tools for the BitTorrent protocol and especially the rTorrent client. It offers the following components:
  * CommandLineTools for automation of common tasks, like metafile creation, and [filtering and mass-changing your loaded torrents](RtControlExamples.md)
  * patches to [improve your rTorrent experience](RtorrentExtended.md), like new commands and canvas coloring
  * rTorrent extensions like a QueueManager and statistics (_work in progress_)
  * a modern and versatile rTorrent web interface (currently on hold)

See the ScreenShotGallery if you want to get a first impression without [installing the software](QuickStartGuide.md).

![http://i.imgur.com/UALM1.png](http://i.imgur.com/UALM1.png)

To get started right away, see the QuickStartGuide. It's also very easy to WriteYourOwnScripts to automate anything that the standard commands can't do. To get in contact and share your experiences with other users of PyroScope, join the [pyroscope-users](http://groups.google.com/group/pyroscope-users) mailing list or the inofficial <a href='irc://irc.freenode.net/rtorrent'><code>#rtorrent</code></a> channel on `irc.freenode.net`.

If you like PyroScope, click on these buttons to support it.
<table border='0'><tr valign='middle'>
<td><br /><img src='http://i.imgur.com/hAdjM.gif' /></td>
<td><wiki:gadget url="http://www.ohloh.net/p/346666/widgets/project_users.xml?style=red" height="100"  border="0" /></td>
<td align='center'><a href='http://youtu.be/Bv-oajBgsSU'><img src='http://i.imgur.com/5FPx5.png' /></a><br />  Demo Video</td>
</tr></table>


# Project Status #
PyroScope is implemented in [Python](http://www.python.org/) using the [Pylons](http://pylonshq.com/) web framework. The main build tool is [Paver](http://www.blueskyonmars.com/projects/paver/), which is based on `setuptools`.

This is the status of various parts of the project:
| **ohloh.net Statistics** | &lt;wiki:gadget url="http://www.ohloh.net/p/346666/widgets/project\_thin\_badge.xml" height="36"  border="0" /&gt; |
|:-------------------------|:-------------------------------------------------------------------------------------------------------------------|
| **CommandLineTools** | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) mktor, lstor, chtor, rtcontrol, rtxmlrpc, rtmv, pyroadmin |
| **UserConfiguration** | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) loaded from `config.ini` and `config.py` |
| **QueueManager** | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) Working job scheduler, with queue manager and inotify watcher implemented |
| **Web Interface** | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) usable alpha |
| _Torrents List_ | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) all rTorrent views plus active torrents & messages view |
| _Torrent Control_ | _not yet implemented_ |
| _Torrent Detail_ | _not yet implemented_ |
| _Torrents Search_ | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) view filter searching in all metadata fields |
| _Statistics_ | ![http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png](http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png) tracker stats |
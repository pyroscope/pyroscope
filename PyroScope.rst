Introduction
============

PyroScope is a collection of tools for the BitTorrent protocol and
especially the rTorrent client. It offers the following components: \*
CommandLineTools for automation of common tasks, like metafile creation,
and `filtering and mass-changing your loaded
torrents <RtControlExamples.md>`_ \* patches to `improve your rTorrent
experience <RtorrentExtended.md>`_, like new commands and canvas
coloring \* rTorrent extensions like a QueueManager and statistics
(*work in progress*) \* a modern and versatile rTorrent web interface
(currently on hold)

See the ScreenShotGallery if you want to get a first impression without
`installing the software <QuickStartGuide.md>`_.

.. figure:: http://i.imgur.com/UALM1.png
   :align: center
   :alt: http://i.imgur.com/UALM1.png

   http://i.imgur.com/UALM1.png
To get started right away, see the QuickStartGuide. It's also very easy
to WriteYourOwnScripts to automate anything that the standard commands
can't do. To get in contact and share your experiences with other users
of PyroScope, join the
`pyroscope-users <http://groups.google.com/group/pyroscope-users>`_
mailing list or the inofficial #rtorrent channel on
``irc.freenode.net``.

If you like PyroScope, click on these buttons to support it.

.. raw:: html

   <table border='0'><tr valign='middle'>
   <td>

.. raw:: html

   </td>
   <td>

.. raw:: html

   </td>
   <td align='center'>

 Demo Video

.. raw:: html

   </td>
   </tr></table>

Project Status
==============

PyroScope is implemented in `Python <http://www.python.org/>`_ using the
`Pylons <http://pylonshq.com/>`_ web framework. The main build tool is
`Paver <http://www.blueskyonmars.com/projects/paver/>`_, which is based
on ``setuptools``.

This is the status of various parts of the project: \| **ohloh.net
Statistics** \| <wiki:gadget
url="http://www.ohloh.net/p/346666/widgets/project\_thin\_badge.xml"
height="36" border="0" /> \|
\|:-------------------------\|:-------------------------------------------------------------------------------------------------------------------\|
\| **CommandLineTools** \|
|http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png|
mktor, lstor, chtor, rtcontrol, rtxmlrpc, rtmv, pyroadmin \| \|
**UserConfiguration** \| |image1| loaded from ``config.ini`` and
``config.py`` \| \| **QueueManager** \| |image2| Working job scheduler,
with queue manager and inotify watcher implemented \| \| **Web
Interface** \| |image3| usable alpha \| \| *Torrents List* \| |image4|
all rTorrent views plus active torrents & messages view \| \| *Torrent
Control* \| *not yet implemented* \| \| *Torrent Detail* \| *not yet
implemented* \| \| *Torrents Search* \| |image5| view filter searching
in all metadata fields \| \| *Statistics* \| |image6| tracker stats \|

.. |http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image1| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image2| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image3| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image4| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image5| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png
.. |image6| image:: http://pyroscope.googlecode.com/svn/trunk/pyroscope/docs/media/img/box-check.png

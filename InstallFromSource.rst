    ➽ *If you want to **update** your already installed software, go to
    the MigrationGuide instead!*

Installing from source
======================

If you have experience with the shell prompt and possibly a bit of
Python you might want to install the development version to gain early
access to new features. Since that version is constantly used in cron
jobs, chances that it is unstable at any point in time are slim. Please
**monitor the `SVN
log <http://code.google.com/p/pyroscope/source/list>`_ and the
`changelog <http://code.google.com/p/pyroscope/source/browse/trunk/debian/changelog>`_**
if you run from source.

For a working installation, you have to meet these requirements first:
\* Python 2.5 or a higher 2.x version (2.6 is recommended). \* A proper
build environment and a subversion + git client. On Debian and Ubuntu,
you'll need the following packages installed (if there are packages
missing from that list, please leave a comment):
``aptitude install python python-dev build-essential subversion git`` \*
For ``rtcontrol`` and ``rtxmlrpc``, an existing rTorrent installation,
*with the xmlrpc option compiled in* and the ``scgi_local`` or
``scgi_port`` command added to your ``~/.rtorrent.rc``. \* Using
rTorrent **0.9.2**, **0.8.9** or **0.8.6** is recommended — PyroScope
*should* work together with older versions though, up to a point.

Initial installation to ``~/lib/pyroscope`` is as follows (do **NOT** do
this as ``root`` or using ``sudo``):
``# To be executed in a shell with your normal user account! mkdir -p ~/bin ~/lib svn checkout http://pyroscope.googlecode.com/svn/trunk/ ~/lib/pyroscope ~/lib/pyroscope/update-to-head.sh # pass "/usr/bin/python2" or whatever to the script, if "/usr/bin/python" is not a suitable version``

After that, the CommandLineTools are available in the
``~/lib/pyroscope/bin`` directory, and also added to your user's bin
directory. And yes, this requires you to `add ~/bin to your
PATH <http://linux.about.com/od/linux101/l/blnewbie3_1_4.htm>`_, if you
didn't do that yet. To finish installation, read the next section.

Completing your setup
=====================

After installation, you **must change your ``rtorrent.rc``** using the
instructions on the UserConfiguration page, else many features of
``rtcontrol`` won't work as expected. You should at least **create a
configuration** as described there, using the
``pyroadmin --create-config`` command. If you encounter any problems
during installation not covered by the documentation, subscribe to the
`pyroscope-users <http://groups.google.com/group/pyroscope-users>`_
mailing list to get help from the community, or join the inofficial
##rtorrent channel on ``irc.freenode.net``.

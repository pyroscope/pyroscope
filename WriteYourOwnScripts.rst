Introduction
============

The ``pyrocore`` Python package contains powerful helper classes that
make remote access to rTorrent child's play (see `API
documentation <http://packages.python.org/pyrocore/apidocs/index.html>`_).
And your tools get the same Look & Feel like the built-in PyroScope
commands, as long as you use the provided base class
`ScriptBaseWithConfig <http://packages.python.org/pyrocore/apidocs/pyrocore.scripts.base.ScriptBaseWithConfig-class.html>`_.

See for yourself: \`\`\` #! /usr/bin/env python

Enter the magic kingdom
=======================

from pyrocore import config from pyrocore.scripts import base

class UserScript(base.ScriptBaseWithConfig): """ Just some script you
wrote. """

::

    # argument description for the usage information
    ARGS_HELP = "<arg_1>... <arg_n>"


    def add_options(self):
        """ Add program options.
        """
        super(UserScript, self).add_options()

        # basic options
        ##self.add_bool_option("-n", "--dry-run",
        ##    help="don't do anything, just tell what would happen")


    def mainloop(self):
        """ The main loop.
        """
        # Grab your magic wand
        proxy = config.engine.open()

        # Wave it
        torrents = list(config.engine.items())

        # Abracadabra
        print "You have loaded %d torrents tracked by %d trackers." % (
            len(torrents), 
            len(set(i.alias for i in torrents)),
        )

        self.LOG.info("XMLRPC stats: %s" % proxy)

if **name** == "**main**": base.ScriptBase.setup() UserScript().run()
\`\`\`

Another full example is the `dynamic seed
throttle <https://pyroscope.googlecode.com/svn/trunk/pyrocore/docs/examples/rt_cron_throttle_seed>`_
script.

For simple calls, you can also use the ``rtxmlrpc`` command on a shell
prompt, see RtXmlRpcExamples for that. For a reference of the rTorrent
XMLRPC interface, see RtXmlRpcReference. Another common way to add your
own extensions is to define CustomFields, usable by ``rtcontrol`` just
like built-in ones.

Interactive use in a Python shell
=================================

You can also access rTorrent interactively, like this:
``>>> from pyrocore import connect >>> rt = connect() >>> len(set(i.tracker for i in rt.items())) 2 >>> rt.engine_software 'rTorrent 0.9.2/0.13.2' >>> rt.uptime 1325.6771779060364 >>> proxy = rt.open() >>> len(proxy.system.listMethods()) 1033``

Using ``pyrocore`` as a library in other projects
=================================================

The example in the first section is an easy way to create user-defined
scripts. If you want to use ``pyrocore``'s features in another runtime
environment, you just have to load the configuration manually (what
`ScriptBaseWithConfig <http://packages.python.org/pyrocore/apidocs/pyrocore.scripts.base.ScriptBaseWithConfig-class.html>`_
does for you otherwise). \`\`\` # Details depend on the system you want
to extend, of course from some\_system import plugin from pyrocore
import error from pyrocore.util import load\_config

def my\_rtorrent\_plugin(): """ Initialize plugin. """ try:
load\_config.ConfigLoader().load() except error.LoggableError, exc: #
Handle accordingly... else: # Do some other stuff...

plugin.register(my\_rtorrent\_plugin) \`\`\`

You can also take a look at the `FlexGet
plugins <http://code.google.com/p/pyroscope/source/browse/trunk#trunk%2Fpyrocore%2Fsrc%2Fpyrocore%2Fflexget>`_
for concrete examples.

Code snippets
=============

*Note that the following snippets are meant to be placed and executed
within the ``mainloop`` of the above script skeleton.*

Accessing the files in a download item
--------------------------------------

To get all the files for several items at once, we combine
``system.multicall`` and ``f.multicall`` to one big efficient mess. :D
\`\`\` from pprint import pprint, pformat

The attributes we want to fetch
===============================

methods = [ "f.get\_path", "f.get\_size\_bytes", "f.get\_last\_touched",
"f.get\_priority", "f.is\_created", "f.is\_open", ]

Build the multicall argument
============================

f\_calls = [method + '=' for method in methods] calls = [{"methodName":
"f.multicall", "params": [infohash, 0] + f\_calls} for infohash in
self.args ]

Make the calls
==============

multicall = proxy.system.multicall result = multicall(calls)

Print the results
=================

for infohash, (files,) in zip(self.args, result): print ("\ :sub:`~`\ 
%s [%d file(s)] " % (infohash, len(files))).ljust(78, '~') pprint(files)
self.LOG.info("Multicall stats: %s" % multicall) \`\`\`

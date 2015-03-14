

# Introduction #

After you installed the software as outlined on QuickStartGuide, you need to add personal configuration that is loaded from the directory `~/.pyroscope` containing the files `config.ini` and `config.py`. A default set can be automatically created for you, see below for details.

**➽ IMPORTANT: For a fresh installation in addition to an existing rTorrent one, you will also need to follow the ["migration" instructions](MigrationGuide.md), which fill in some data your already running rTorrent instance is missing otherwise.**

For simple setups, you only need to edit the plain text file `config.ini`. The script `config.py` allows much more detailed control over complex setups, at the price of you knowing at least the basics of the Python programming language.

If you have any problems with or questions about your configuration, subscribe to the [pyroscope-users](http://groups.google.com/group/pyroscope-users) mailing list to get help from the community, or join the inofficial <a href='irc://irc.freenode.net/rtorrent'><code>#rtorrent</code></a> channel on `irc.freenode.net`.


# Creating a set of default configuration files #

To create your own configuration, the best way is to start from the default files that are part of your PyroScope installation. To create them at the default location `~/.pyroscope`, simply call this command:
```
pyroadmin --create-config
```
Note that you can delete anything you don't want changed, since the defaults are _always_ loaded first. Deleting unchanged defaults has the advantage that on software updates, you'll automatically get the newer version of settings, if they're updated.

If you need several distinct configuration sets, just add the `--config-dir` option like so:
```
pyroadmin --create-config --config-dir ~/rtorrent/special/.pyroscope
```

To view your configuration, use this (again, use the `--config-dir` option for non-default configurations):
```
pyroadmin --dump-config
```


# Setting values in `config.ini` #

The configuration file consists of sections, led by a `[section]` header and followed by `name: value` entries; `name = value` is also accepted. Longer values can be broken into several lines and the continuation lines must be indented (start with a space). Note that leading whitespace is removed from values.

Lines beginning with a semicolon (`;`), a hash mark (`#`), or the letters `REM` (uppercase or lowercase) will be ignored and can be used for comments. You cannot put a comment on an option line, a comment **MUST** start the beginning of a line!

As an example, this is a very minimal configuration file:
```
# PyroScope configuration file

[GLOBAL]
# Note that the "config_dir" value is provided by the system!
config_script = %(config_dir)s/config.py
rtorrent_rc = ~/.rtorrent.rc

[ANNOUNCE]
# Add alias names for announce URLs to this section; those aliases are used
# at many places, e.g. by the "mktor" tool

# Public trackers
PBT     = http://tracker.publicbt.com:80/announce
          udp://tracker.publicbt.com:80/announce
OBT     = http://tracker.openbittorrent.com:80/announce
          udp://tracker.openbittorrent.com:80/announce
Debian  = http://bttracker.debian.org:6969/announce
```

_For advanced users:_ Values can contain format strings of the form `%(name)s` which refer to other values in the same section, or values in the `[DEFAULT]` section.

# Extending your `.rtorrent.rc` #

You need either a `scgi_local` or `scgi_port` specification in your rTorrent configuration; `scgi_local` is preferable since more secure. Furthermore, you need to provide the path to a `session` directory. See the [rTorrent man page](http://libtorrent.rakshasa.no/rtorrent/rtorrent.1.html) for details.

<a></a>
For the `loaded` and `completed` fields to work, as well as the `started`, `leechtime` and `seedtime` ones, you also have to add these commands (note that most settings actually reside in an [included file](http://pyroscope.googlecode.com/svn/trunk/pyrocore/src/pyrocore/data/config/rtorrent-0.8.6.rc)):
```
#
# PyroScope SETTINGS
#

# Set "pyro.extended" to 1 to activate rTorrent-PS features!
# LEAVE THIS AT 0 IF YOU RUN A VANILLA rTorrent!
system.method.insert = pyro.extended, value|const, 0

# Set "pyro.bin_dir" to the "bin" directory where you installed the pyrocore tools!
# Make sure you end it with a "/"; if this is left empty, then the shell's path is searched.
system.method.insert = pyro.bin_dir, string|const, 

# Remove the ".default" if you want to change something (else your 
# changes get over-written on update).
system.method.insert = pyro.rc_dialect, string|const|simple, "execute_capture=bash,-c,\"test $1 = 0.8.6 && echo -n 0.8.6 || echo -n 0.8.9\",dialect,$system.client_version="
system.method.insert = pyro.rtorrent_rc, string|const|private, "$cat=~/.pyroscope/rtorrent-,\"$pyro.rc_dialect=\",.rc.default"
import = $pyro.rtorrent_rc=

# TORQUE: Daemon watchdog schedule
# Must be activated by touching the "~/.pyroscope/run/pyrotorque" file!
# Set the second argument to "-v" or "-q" to change log verbosity.
schedule = pyro_watchdog,30,300,"pyro.watchdog=~/.pyroscope,"
```
See this [rtorrent.rc](DebianInstallFromSource#rTorrent_configuration.md) for a complete example, including some view changes made possible by the additional custom fields.

**Note that if you just freshly installed PyroScope into an existing rTorrent installation, you must also follow the ["migration" instructions](MigrationGuide.md) to add missing data to your already loaded downloads. Else, those items will NOT be filtered correctly.**

If you run rTorrent 0.8.7 and up, you **must** read RtXmlRpcMigration.


# Modifying and extending your configuration via `config.py` #

## Defining your own custom fields ##
You can add user-defined fields to `~/.pyroscope/config.py` that behave just like the built-in ones, for more details on that see CustomFields.
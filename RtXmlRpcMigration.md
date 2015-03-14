

# Changes after 0.8.7 #
Version 0.8.7 is the last version that supports the "old" command set, see the [rTorrent community wiki](http://wiki.rtorrent.org/RtorrentMigration#Version_0.8.6_to_0.8.7) for more.
PyroScope reasonably supports version 0.8.7 starting with **[revision 1407](https://code.google.com/p/pyroscope/source/detail?r=1407)**, though in that revision not all functions are tested yet (basic selection and the default output format works).
Please use the `-D -K` command line switches to start rTorrent.
Also take into account that any web interfaces like ruTorrent need to be updated at the same time as the rest of your installation, refer to their documentation on how to do that and which version to choose.

To convert your configuration in `~/.rtorrent.rc` to the new commands, there is a **[migration script](https://pyroscope.googlecode.com/svn/trunk/pyrocore/src/scripts/migrate_rtorrent_rc.sh)** available that mostly automates the process. Just download it and call it like this:
```
bash migrate_rtorrent_rc.sh ~/.rtorrent.rc
pyroadmin --create-config 
```
A backup of your old configuration is created automatically.

Also, look into `~/.pyroscope/config.ini.default` to see how to map commands (in the `[XMLRPC*]` sections).
Please add any additional commands you need to map in your installation as a comment to this page, and also provide the command you called and some version information if possible (SVN revision).


# Bits & pieces from the mailing list #

`execute2`, when called through XMLRPC, requires a target as the first argument, while the old `execute` doesn't. In the future, all XMLRPC commands will require them for consistency, so once clients have had time to move to the new syntax the old one will be disabled by default, except for config files (and the new ones renamed).

On completion moving and order of steps: The official way is that a call to `d.close.directly` (will be in SVN next commit) must precede any commands that move around files, and since setting a new directory does that it is safe to call set new directory before move. However the reverse will cause problems.
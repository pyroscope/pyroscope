

**➽ IMPORTANT: For a fresh installation in addition to an existing rTorrent one, you will also need to follow the instructions here, which fill in some data your already running rTorrent instance is missing otherwise!**

# Making backups #
Since repairing broken files resulting from faulty updates usually is either a lot of work or simply impossible, always **make a backup**. Backups should be made when _either_ PyroScope or rTorrent is changed to a new version or SVN revision.

These steps should make a copy of pretty much anything important:
  1. Copy your rTorrent session data (rTorrent needs to be running):
```
rtxmlrpc -q session_save
tar cvfz /tmp/session-backup-$(date +'%Y-%m-%d').tgz $(echo $(rtxmlrpc get_session)/ | tr -s / /)*.torrent
```
  1. Backup your current PyroScope virtualenv and configuration:
```
tar cvfz /tmp/pyroscope-$(date +'%Y-%m-%d').tgz  ~/.pyroscope/ ~/lib/pyroscope/
```
  1. Depending on how you install rTorrent, make a copy of the rTorrent executable. Note that the `rTorrent-PS` build script installs into versioned directories, i.e. using that you don't have to worry if changing the rTorrent version ­— the old one is still available.


# Updating the software #
**Before** adapting and extending your configuration to make use of new features, you first have to update the software itself. How to do that depends on the way you initially installed it, so follow **one** of the following sections, depending on whether you did a release installation or one from source.


## How to do a release version software update ##

Remember to read the **migration instructions** further below, and the [changelog](http://code.google.com/p/pyroscope/source/browse/trunk/debian/changelog), BEFORE installing any new version**.**

Then to **update** an existing installation, use this command **if** you used the instructions on the InstallReleaseVersion page:
```
sudo easy_install --prefix /usr/local -U pyrocore
```

**Otherwise**, in case you followed InstallToPythonVirtualenv, use this **instead**:
```
~/lib/pyroscope/bin/easy_install -U pyrocore
ln -nfs $(grep -l 'entry_point.*pyrocore==' ~/lib/pyroscope/bin/*) ~/bin/
```

Now **skip** the next section describing a source installation upgrade, and go to the configuration update further below.


## How to update a source installation to the newest code ##

**BEFORE** any update, remember to read the **migration instructions** further below, the **[changelog](http://code.google.com/p/pyroscope/source/browse/trunk/debian/changelog)** and the **[SVN log](http://code.google.com/p/pyroscope/source/list).**

Then to **update** an existing installation, use these commands:
```
cd ~/lib/pyroscope
svn update
./update-to-head.sh
```


# Updating your existing configuration for a new software version #

After you installed a new version of the software, you can easily check whether the default configuration files changed by calling the `pyroadmin --create-config` command. Since this will never overwrite existing configuration files, the files `config.ini.default` and `config.py.default` will be created instead.

You can then use the `diff` tool to check for the differences between your current configuration and the new default one, and add any changes you want to adopt. Also note that sections of the configuration you leave out, and keys that you do not overwrite, are automatically taken from the defaults, which greatly simplifies any update — so having a minimal configuration with just the changes and additions you actually want is recommended.

And remember to **always read the [changelog](http://pyroscope.googlecode.com/svn/trunk/debian/changelog)**!

## Migrating to version 0.3.4 ##
**NOTE: These instructions also apply if you freshly installed version 0.3.4 or higher!**

To fully make use of the new features, you need to do the following:
  1. Read and follow the section _Extending your `.rtorrent.rc`_ on the UserConfiguration page and restart rTorrent.
  1. To add the new custom keys to your existing session data, call these commands in a shell:
```
# Make a full, current backup of the session data
rtxmlrpc -q session_save
tar cvfz ~/session-backup-0.3.4.tgz $(echo $(rtxmlrpc get_session)/ | tr -s / /)*.torrent

# Set missing "loaded" times to that of the .torrent file
rtcontrol '!*"*' loaded=0 -q -sname -o 'echo "$(name)s"\ntest -f "$(metafile)s" && rtxmlrpc -q d.set_custom $(hash)s tm_loaded \$(\
    ls -l --time-style "+%%s" "$(metafile)s" \
    | cut -f6 -d" ")\nrtxmlrpc -q d.save_session $(hash)s' | bash

# Set missing "completed" times to that of the data file or directory
rtcontrol '!*"*' completed=0 done=100 path=\! is_ghost=no -q -sname -o 'echo "$(name)s"\ntest -e "$(realpath)s" && rtxmlrpc -q d.set_custom $(hash)s tm_completed \$(\
    ls -ld --time-style "+%%s" "$(realpath)s" \
    | cut -f6 -d" ")\nrtxmlrpc -q d.save_session $(hash)s' | bash
```
  1. Call `pyroadmin --create-config` and check your `config.ini` against `config.ini.default` as described above. Among other things, the default `output_format` has changed.
  1. The command "`rtcontrol completed=-1d -scompleted`" should now show your completed downloads of the last 24 hours, in order.
  1. Enjoy.

## Migrating to version 0.3.6 ##
To fully make use of the new features, you need to change your rTorrent configuration and execute a few commands. Users that did **not** yet follow the 0.3.4 migration instructions should do so **first**.

**NOTE: These instructions also apply if you freshly installed version 0.3.6 or higher!**

After you're "on the 0.3.4 level", this will get you ready for 0.3.6:
  1. Make a full, current backup of the session data:
```
rtxmlrpc -q session_save
tar cvfz ~/session-backup-0.3.6.tgz $(echo $(rtxmlrpc get_session)/ | tr -s / /)*.torrent
```
  1. Read and follow the section _Extending your `.rtorrent.rc`_ on the UserConfiguration page and restart rTorrent. Users that already added the extensions for previous versions should replace the relevant parts of their configuration with the new snippets.
  1. Call `pyroadmin --create-config` and check your `config.ini` against `config.ini.default` as described above. Among other things, some output formats have changed.
  1. The command "`rtcontrol \* -qostarted | sort | uniq -c`" should now, for the majority of your torrents, show the start time of rTorrent after adding the `tm_started` configuration bits (cf. step 2, stopped ones will get counted under `1970-01-01`).
  1. Assuming you have incomplete torrents, "`rtcontrol is_complete=0 -ostarted.raw.delta,leechtime,name --column-headers`" should show identical values in the `STARTED` and `LEECHTIME` columns.
  1. Enjoy.


## Migrating to version 0.4.1 ##
There is a new dependency on the `pyrobase` package, and for **release version installations**, it will be managed transparently — you have nothing to worry about, just follow the updating instructions from InstallReleaseVersion, and then see below for the required steps after updating.

On the other hand, if you have an **installation from source**, it's important that you add the new dependency _also_ from source, because otherwise your installation will break during further development (since then, you'd remain on the _released_ version of `pyrobase`). So, call these commands (assuming the standard installation paths):
```
cd ~/lib/pyroscope
source bin/activate
svn update
git clone git://github.com/pyroscope/pyrobase.git pyrobase
( cd pyrocore && source bootstrap.sh )
```

In addition, follow these steps:
  1. You **must** add the new `startup_time` command, and you _should_ add the `cull` command (see _Extending your `.rtorrent.rc`_ on the UserConfiguration page).
  1. Call `pyroadmin --create-config` to add the new builtin [Tempita templates](OutputTemplates.md) to your configuration.
  1. To get bash completion for the PyroScope commands, see the instructions on the BashCompletion page.


## Migrating to version 0.4.2 ##

Release 0.4.2 not only contains some additions to the PyroScope commands, but also offers you to run an [extended rTorrent distribution](RtorrentExtended.md) with many user interface and command improvements. You need to decide whether you want to run that version, it involves compiling your own rTorrent executable, but there is a build script that mostly automates the process.

But first, to upgrade your existing installation, follow these steps:
  1. For people that run a source code installation. use the new `update-to-head.sh` script as outlined further up on this page.
  1. Call `pyroadmin --create-config` to update the `.default` configuration examples, and also to create the new `.rtorrent.rc` include (see next step).
  1. Read the section _Extending your `.rtorrent.rc`_ on the UserConfiguration page again! There is a new standard configuration include, which greatly simplifies integrating additional PyroScope settings into your main configuration. Add that include as shown there, and take care to remove anything from the main `.rtorrent.rc` that's already added by the include, else you get error messages on startup, or worse, inconsistent behaviour.
  1. Restart rTorrent and try to do a search using `^X s=x264` or another keyword you expect some hits on. If that works, you can be pretty sure everything's OK

The new stable version 0.8.9 of rTorrent is now supported by this release, see RtXmlRpcMigration for details.


## Migrating to version 0.4.3 ##

The 0.4.3 release adds a QueueManager and (possibly) EventHandling.

To upgrade your existing installation, follow these steps:
  1. For people that run a source code installation. use the `update-to-head.sh` script as usual, outlined further up on this page.
  1. Call `pyroadmin --create-config` to update the `.default` configuration examples.
  1. Read the QueueManager and EventHandling pages if you plan to use these features; both are inactive by default and  need to be enabled.
    * You need to add the new `pyro_watchdog` schedule into your configuration, as shown on the UserConfiguration page.

If you upgraded to rTorrent **0.9.2**, take note of the new way the PyroScope configuration include is loaded, see [here](UserConfiguration#Extending_your_.rtorrent.rc.md) (the block containing the `pyro.rc_dialect` command is updated).
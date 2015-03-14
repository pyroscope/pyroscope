

**⚠ IMPLEMENTATION STATUS:** In SVN head, the following is implemented:
  * the "filter" plugins, but docs need to be written
  * "torrent\_view" needs some refactoring for better configuration (no globals)


# Configuration steps to activate the rTorrent plugins #
To add the PyroScope plugins to your FlexGet installation, you just need to execute the following commands:
```
mkdir -p ~/.flexget/plugins
echo "from pyrocore.flexget import *" >~/.flexget/plugins/pyroflex.py
```
Check whether this worked by running the command `flexget --doc rtorrent`.

**⚠ IMPORTANT:** Note that you need to run a reasonably recent FlexGet 1.0 beta installation to successfully use these plugins. More on setting up FlexGet can be found on its [homepage](http://flexget.com/wiki/Install).
Also, both FlexGet and PyroScope need to be installed into the system Python interpreter, or alternatively the same virtualenv.
In case you have different environments set up for FlexGet and PyroScope (via InstallToPythonVirtualenv), you can easily add that existing installation to a different FlexGet virtualenv, like this:
```
. ~/lib/flexget/bin/activate 
easy_install -U "setuptools>=0.6c11"
easy_install -U "paver>=1.0"
cd ~/lib/pyroscope
( cd pyrobase && paver develop -U )
( cd pyrocore && paver develop -U )
```


# Loading accepted items directly into rTorrent #
## Introduction to the `rtorrent` plugin ##
The `rtorrent` plugin is probably the one most useful to people that use both rTorrent and FlexGet. It's a FlexGet output plugin similar to the [Deluge one](http://flexget.com/wiki/Plugins/deluge) that ...

**TODO:** More details...
  * Connection settings
  * Custom fields
  * Defaults


## `rtorrent` options ##
The following options can be used to configure the plugin's behaviour. Many of them have semantics identical to that of the [Deluge plugin](http://flexget.com/wiki/Plugins/deluge#Options), making it easier to share configurations.

| **Name** | **Default** | **Description** |
|:---------|:------------|:----------------|
| `connection` | from `~/.rtorrent.rc` | The SCGI connection URL for the client. |
| `path` | from `~/.rtorrent.rc` | The download location (directory). |
| `movedone` | Don't move (unset) | The location the downloaded data will be moved to on completion. The rules regarding target paths as described for [rtmv](CommandLineTools#rtmv.md) do apply. **TODO: find out where rutorrent stores this** |
| `cmd_done` | None | A specific command that will be executed on completion. See the following section for details. |
| `start` | `yes` | Start items immediately? |
| `ignore` | `no` | Set item to ignore commands? |
| `label` | `???` | Set custom field "`label`". **TODO: find out where rutorrent stores this** |
| `fields` | No custom fields | List of custom fields to set. **TODO: Details / Examples** |
| `throttle` | `none` | Name of throttle group to put items into (`null` = unlimited, `none` = global). |
| `` | `` | ... more? **TODO** |

Note that many of the above settings can be used on a per-entry basis, if you add them e.g. via the `settings` plugin. **NOT IMPLEMENTED YET / LIST THEM**


## Necessary `~/.rtorrent.rc` extensions ##
For the `movedone` and `cmd_done` options to work as expected, you need some additions to your `~/.rtorrent.rc` of course. The easiest way to achieve that is adding these lines: **TODO**
```
...
```
Note that the support for `cmd_done` needs to be enabled explicitely, since it can pose a security risk, especially when you're not the only one with access to your FlexGet configuration (e.g. via the web UI). In such cases, you're better off with setting some custom value, on which a statically configured script can react accordingly. (**TODO** how enable it?)


## Advanced usage ##
As with the Deluge plugin, you can [use the settings plugin](http://flexget.com/wiki/Cookbook/Series/DelugeMovedone) to add custom fields to any entry, which are then used by the rTorrent plugin. **NOT IMPLEMENTED YET**


## Configuration examples ##

Recommended configuration: **TODO**
```
presets:
  global:
    torrent_scrub: rtorrent

feeds:
  recommended:
    rtorrent: yes
    ...
```

More examples: **TODO**
```
feeds:
  using_defaults:
    rtorrent: yes
    ...
```


# Filtering entries based on rTorrent's status #

The `rtorrent_filter` plugin allows you to reject items based on what's already loaded into your client.

**TODO:** More details...

Examples: **TODO**
```
feeds:
  using_defaults:
    rtorrent_filter: yes
    ...
```


# Using items loaded into rTorrent as a feed #

**TODO:** More details...


# Using filter expressions #

**TODO:** Describe syntax extensions in more detail.
Link to FlexGet page with fields listing.

Plugins: pyro\_reject\_if, pyro\_accept\_if, pyro\_reject\_if\_download, pyro\_accept\_if\_download


Examples:
```
feeds:
  good_movies:
    pyro_accept_if: rating>9
    ...
  good_or_new_movies:
    pyro_accept_if:
      - year>=2010
      - rating>9
    ...
  public_torrent_downloads_only:
    pyro_reject_if_download: ?torrent.content.info.?private=1
    ...
  ubuntu_offical:
    pyro_accept_if_download: ?torrent.content.announce=*.ubuntu.com[/:]*
    ...
  quality_name:
    pyro_reject_if: quality.name~(1080|720)p
    ...
  quality_level:
    pyro_reject_if: quality.value<500
    ...
```
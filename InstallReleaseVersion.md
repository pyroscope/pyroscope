**Use InstallFromSource, the release version is out of date**

---





> ➽ _If you want to **update** your already installed software, go to the MigrationGuide instead!_

# Installing a release version #
For a working installation, you have to meet these requirements first:
  * Python 2.5 or a higher 2.x version (2.6 is recommended); go to http://www.python.org/download/ if you're on an OS that doesn't have Python out of the box.
  * for `rtcontrol` and `rtxmlrpc`, an existing rTorrent installation, _with the xmlrpc option compiled in_ and the `scgi_local` or `scgi_port` command added to your `~/.rtorrent.rc`.
  * Using rTorrent **0.9.2**, **0.8.9** or **0.8.6** is recommended — PyroScope _should_ work together with older versions though, up to a point.

On Debian, Ubuntu, and other Debian-derived distributions, do this:
```
sudo apt-get install python-setuptools
sudo easy_install --prefix /usr/local pyrocore
```
After that, the CommandLineTools should be immediately available in your shell prompt.

In case you have no `root` rights, or `easy_install` prints a message containing »`error: bad install directory or PYTHONPATH`«, try to InstallToPythonVirtualenv instead, and after having done so, return to this page and read on. Do **not** try to repeat the above commands.


# Completing your setup #
To complete your setup, you **must change your `rtorrent.rc`** using the instructions on the UserConfiguration page, else many features of `rtcontrol` won't work as expected. You should at least **create a configuration** as described there, using the `pyroadmin --create-config` command. If you encounter any problems during installation not covered by the documentation, subscribe to the [pyroscope-users](http://groups.google.com/group/pyroscope-users) mailing list to get help from the community, or join the inofficial <a href='irc://irc.freenode.net/rtorrent'><code>#rtorrent</code></a> channel on `irc.freenode.net`.


# Special considerations for different platforms #

## Machines you have no adminstration (root) rights for ##
If you miss the right to globally install any software, there's still hope, as long as any version of Python 2.5, 2.6 or 2.7 is installed already (call the command `python --version` to check).

In such a case, just follow InstallToPythonVirtualenv to add everything else that you need to your own account.

## Debian, Ubuntu, and other Debian-derived distributions ##

Nothing special, just see the first section of this page.

## Arch Linux ##

See this [AUR package](https://aur.archlinux.org/packages.php?ID=47197) and take note of the hints regarding configuration, in the "_Completing your setup_" section of this page.


## Other Linux variants and Mac OSX ##

For non-Debian distributions, use the appropriate package management tools to install the aforementioned prerequisites — the package names should be similar (contain the word "`setuptools`"). If you're unable to find a `setuptools` package for your distribution, download it [from here](http://pypi.python.org/pypi/setuptools/) and install it according to the given instructions.

Then use the `easy_install` command shown in the first section to download and install the `pyrocore` package, and take note of the hints regarding configuration in the "_Completing your setup_" section of this page..


## Windows ##

On Windows, just use `easy_install pyrocore` in `cmd.exe` after [installing Python](http://www.python.org/download/) and `setuptools` as [described here](http://pypi.python.org/pypi/setuptools/).

Note that on Windows, you are limited to using the tools that allow the handling of torrent files. There seems to be a Cygwin port of rTorrent for Windows, but there are no reports yet of any such installation working together with PyroScope.
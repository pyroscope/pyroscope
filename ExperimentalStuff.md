
---

**What follows is the more complex installation of the yet-incomplete web interface and currently has a chance of being broken...**

---


# Installing the web interface #

Currently, the only way to install and use the web interface is from source, so you first need to follow the "_Installing from source (SVN)_" section above. Note that the web-ui is currently unsupported and on hold — if it doesn't work for you, it just doesn't.

_The file system paths in the following sections can be adapted to your installation, of course, but avoid that unless you have a good reason. It's recommended to put the SCGI socket into the `~/lib/rtorrent` directory, just create it if your rTorrent installation is located elsewhere. These instructions work best if PyroScope is installed into the same user account as rTorrent._

## `PyroScope` basic configuration ##
Set up the `pyroscope` subproject, create the `~/.pyroscope` directory and the necessary sub directories.
```
cd ~/lib/pyroscope/pyroscope
source bootstrap.sh
mkdir -p ~/.pyroscope/{log,data,www-data}
```

## Starting the web interface ##
To use the web server, you first have to make a config file as follows:
```
cd ~/lib/pyroscope/pyroscope
../bin/paster make-config pyroscope ~/.pyroscope/web.ini
```

Tweak the config file as appropriate (read the comments in the file); if you intend to use the default port 8042 this can be skipped altogether. Then start the web server in daemon mode:
```
cd ~/lib/pyroscope/pyroscope
../bin/paver start
```
If you did not change the web server parameters, you can now view the start page at http://127.0.0.1:8042/. You can use the `paver status` command to check on the server status, and `paver stop` to stop a running server.

## Updating the WEB-UI to the latest SVN revision ##
To update the software including the web-ui after initial installation, use these commands:
```
cd ~/lib/pyroscope
source bin/activate
( cd pyroscope && paver stop )
svn update
( cd pyrocore && source bootstrap.sh )
( cd pyroscope && paver develop -U && paver bootstrap && paver start )
```


# Enabling the queue manager #
**NOT IMPLEMENTED YET**

Using `crontab -e`, add the following to your cron schedule:
```
* * * * *   test -S ~/lib/rtorrent/.scgi_local && ~/lib/pyroscope/bin/pyro-qm
```
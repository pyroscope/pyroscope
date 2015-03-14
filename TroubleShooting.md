## Python Diagnostics ##

Execute the following command to be able to provide some information on your Python installation:

```
deactivate 2>/dev/null; /usr/bin/virtualenv --version; python <<'.'
import sys, os, time, pprint
pprint.pprint(dict(
    version=sys.version,
    prefix=sys.prefix,
    os_uc_names=os.path.supports_unicode_filenames,
    enc_def=sys.getdefaultencoding(),
    maxuchr=sys.maxunicode,
    enc_fs=sys.getfilesystemencoding(),
    tz=time.tzname,
    lang=os.getenv("LANG"),
    term=os.getenv("TERM"),
    sh=os.getenv("SHELL"),
))
.
```

If `enc_fs` is **not** `UTF-8`, then call `dpkg-reconfigure locales` (on Debian type systems) and choose a proper locale (you might also need `locale-gen en_US.UTF-8`), and make sure `LANG` is set to `en_US.UTF-8` (or another locale with UTF-8 encoding).


## OS Diagnostics ##
Similarly, execute this in a shell prompt:

```
uname -a; echo $(lsb_release -as 2>/dev/null); grep name /proc/cpuinfo | uniq -c; \
free -m | head -n2; uptime; \
strings $(which rtorrent) | grep "client version"; \
ldd $(which rtorrent) | egrep "lib(torrent|curses|curl|xmlrpc.so|cares|ssl|crypto)"; \
ps auxw | egrep "USER|/rtorrent" | grep -v grep
```
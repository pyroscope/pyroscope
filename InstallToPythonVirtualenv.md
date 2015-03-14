

# Creating an isolated Python environment in your account #
If you lack the right for global installing, or just wish to keep things separate and limited to your account, the following will allow you to do just that. Note that the `update-to-head.sh` script featured on InstallFromSource already does this for you, so this is just necessary if you insist on running a release version, but cannot write to `/usr/local`.

**⚠ NOTE:** This assumes that any version of Python 2.5, 2.6 or 2.7 is already installed on the machine — call the command `python --version` to check.

First, we create the Python virtual environment (do **NOT** do this as `root` or using `sudo`):
```
mkdir -p ~/bin ~/lib/pyroscope
cd ~/lib/pyroscope
venv='https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
python -c "import urllib2; open('venv.py','w').write(urllib2.urlopen('$venv').read())"
deactivate 2>/dev/null
python venv.py --no-site-packages $(pwd)
```

Now, continue to install a release version **as described in the next section**.

# Installing a release version #

To install a release version into your virtualenv, the next step is all you need for success (do **NOT** do this as `root` or using `sudo`):
```
~/lib/pyroscope/bin/easy_install pyrocore
ln -nfs $(grep -l 'entry_point.*pyrocore==' ~/lib/pyroscope/bin/*) ~/bin/
```
And yes, this requires you to [add ~/bin to your PATH](http://linux.about.com/od/linux101/l/blnewbie3_1_4.htm), if you didn't do that yet. Now head back to [InstallReleaseVersion#Completing\_your\_setup](InstallReleaseVersion#Completing_your_setup.md).
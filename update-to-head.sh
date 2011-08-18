#! /bin/bash
install_venv() {
    venv='https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
    python -c "import urllib2; open('venv.py','w').write(urllib2.urlopen('$venv').read())"
    deactivate 2>/dev/null || true
    python venv.py --no-site-packages .
}

set -e
cd $(dirname "$0")

# People never read docs anyway, so let the machine check...
test $(id -u) -ne 0 || { echo "Do NOT install as root! Read the wiki."; exit 1; }
cat <<'.' | python
import sys
print "Using Python", sys.version
assert sys.version_info >= (2, 5), "Use Python 2.5 or a higher 2.X! Read the wiki."
assert sys.version_info < (3,), "Use Python 2.5, 2.6, or 2.7! Read the wiki."
.
 
echo "Updating your installation..."

# Ensure virtualenv is there
test -f bin/activate || install_venv

# Bootstrap if script was downloaded...
test -d .svn || svn co https://pyroscope.googlecode.com/svn/trunk/pyrocore .

# Get pyrobase initially, for old or yet incomplete installations
test -d pyrobase || { echo "Getting pyrobase..."; git clone "git://github.com/pyroscope/pyrobase.git" pyrobase; }

# Update source
source bin/activate
svn update
( cd pyrobase && git pull -q )
( cd pyrocore && source bootstrap.sh )

# Register new executables
test ! -d ~/bin || ln -nfs $(grep -l 'entry_point.*pyrocore==' $PWD/bin/*) ~/bin/

# Update config defaults
./bin/pyroadmin --create-config 

# Make sure PATH is decent
( echo $PATH | tr : \\n | grep "^$HOME/bin\$" >/dev/null ) || echo "$HOME/bin is NOT on your PATH, you need to fix that"'!'


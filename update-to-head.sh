#! /bin/bash
install_venv() {
    venv='https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
    python -c "import urllib2; open('venv.py','w').write(urllib2.urlopen('$venv').read())"
    deactivate 2>/dev/null || true
    python venv.py --no-site-packages .
}

set -e
cd $(dirname "$0")
echo "Updating your installation..."

# Ensure virtualenv is there
test -f bin/activate || install_venv

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
pyroadmin --create-config 


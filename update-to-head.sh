#! /bin/bash
set -e
cd $(dirname "$0")
echo "Updating your installation..."

# Ensure virtualenv is there
test -f bin/activate || { echo "ERROR: No virtualenv found (./bin/activate missing)"; exit 1; }

# Get pyrobase initially, for old installations
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


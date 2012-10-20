#! /bin/bash
PYTHON=${1:-/usr/bin/python}

install_venv() {
    venv='https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
    $PYTHON -c "import urllib2; open('virtualenv.py','w').write(urllib2.urlopen('$venv').read())"
    deactivate 2>/dev/null || true
    $PYTHON virtualenv.py .
}

git_projects="pyrobase auvyon"

set -e
cd $(dirname "$0")
deactivate 2>/dev/null || true
rtfm="DO read http://code.google.com/p/pyroscope/wiki/InstallFromSource."

# Fix Generation YouTube's reading disability
for cmd in $PYTHON svn git; do
    which $cmd >/dev/null 2>&1 || { echo >&2 "You need a working '$cmd' on your PATH. $rtfm"; exit 1; }
done

# People never read docs anyway, so let the machine check...
test $(id -u) -ne 0 || { echo "Do NOT install as root! $rtfm"; exit 1; }
test -f ./bin/activate && vpy=$PWD/bin/python || vpy=$PYTHON
cat <<'.' | $vpy
import sys
print("Using Python %s" % sys.version)
assert sys.version_info >= (2, 5), "Use Python 2.5 or a higher 2.X! Read the wiki."
assert sys.version_info < (3,), "Use Python 2.5, 2.6, or 2.7! Read the wiki."
.
 
echo "Updating your installation..."

# Ensure virtualenv is there
test -f bin/activate || install_venv

# Bootstrap if script was downloaded...
test -d .svn || svn co http://pyroscope.googlecode.com/svn/trunk .

# Get base packages initially, for old or yet incomplete installations
for project in $git_projects; do
    test -d $project || { echo "Getting $project..."; git clone "git://github.com/pyroscope/$project.git" $project; }
done

# Update source
source bin/activate
svn update
for project in $git_projects; do
    ( cd $project && git pull -q )
done
( cd pyrocore && source bootstrap.sh )
for project in $git_projects; do
    ( cd $project && ../bin/paver develop -U )
done

# Register new executables
test ! -d ${BIN_DIR:-~/bin} || ln -nfs $(grep -l 'entry_point.*pyrocore==' $PWD/bin/*) ${BIN_DIR:-~/bin}/

# Update config defaults
./bin/pyroadmin --create-config 

# Make sure PATH is decent
( echo $PATH | tr : \\n | grep "^$HOME/bin/?\$" >/dev/null ) || echo "$HOME/bin is NOT on your PATH, you need to fix that"'!'


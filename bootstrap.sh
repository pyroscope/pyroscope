# This script has to be sourced in a shell and is thus NOT executable.
if test ! -f ./bin/activate; then
    deactivate 2>/dev/null || true
    virtualenv --no-site-packages . || return 1
fi

export DEBFULLNAME=pyroscope
export DEBEMAIL=pyroscope.project@gmail.com

grep DEBFULLNAME bin/activate >/dev/null || cat >>bin/activate <<EOF
export DEBFULLNAME=$DEBFULLNAME
export DEBEMAIL=$DEBEMAIL
EOF

. bin/activate || return 1
test -x bin/pip || bin/easy_install pip

# tools
./bin/pip install -U "setuptools>=0.6c11" || return 1
./bin/pip install -U "paver>=1.0.5" || return 1
##./bin/pip install -U "nose>=1.0" || return 1
##./bin/pip install -U "coverage>=3.4" || return 1
./bin/pip install -U "yolk>=0.4.1" || return 1
##./bin/pip install -U "PasteScript>=1.7.3" || return 1

# Harmless options (just install them, but ignore errors)
./bin/pip install -U "Tempita>=0.5.1" || :
./bin/pip install -U "APScheduler>=2.0.2" || :
./bin/pip install -U "waitress>=0.8.2" || :
./bin/pip install -U "WebOb>=1.2.3" || :
##./bin/pip install -U "psutil>=0.6.1" || :

# pyrobase
test ! -d pyrobase || ( cd pyrobase && ../bin/paver -q develop -U)


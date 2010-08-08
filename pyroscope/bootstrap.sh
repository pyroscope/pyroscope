# This script has to be sourced in a shell and is thus NOT executable.

# generic bootstrap
if test ! -f ../bin/activate; then
    ( cd .. && . ./bootstrap.sh ) || return 1
fi
. ../bin/activate || return 1

# base packages
if python -c "import pyrocore" 2>/dev/null; then
    echo "Package pyrocore already installed."
else
    ( cd ../pyrocore && . ./bootstrap.sh ) || return 1
fi

# project
paver develop -U || return 1
paver bootstrap || return 1


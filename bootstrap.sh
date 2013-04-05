# This script has to be sourced in a shell and is thus NOT executable.
. ./util.sh # load funcs

test -f ./bin/activate || install_venv --no-site-packages
. ./bin/activate

export DEBFULLNAME=pyroscope
export DEBEMAIL=pyroscope.project@gmail.com

grep DEBFULLNAME bin/activate >/dev/null || cat >>bin/activate <<EOF
export DEBFULLNAME=$DEBFULLNAME
export DEBEMAIL=$DEBEMAIL
EOF

# tools
pip_install -U "setuptools>=0.6c11"
pip_install -U "paver>=1.0.5"
##pip_install -U "nose>=1.0"
##pip_install -U "coverage>=3.4"
pip_install -U "yolk>=0.4.1"
##pip_install -U "PasteScript>=1.7.3"

# Harmless options (just install them, but ignore errors)
pip_install_opt -U "Tempita>=0.5.1"
pip_install_opt -U "APScheduler>=2.0.2"
pip_install_opt -U "waitress>=0.8.2"
pip_install_opt -U "WebOb>=1.2.3"
##pip_install_opt -U "psutil>=0.6.1"

# pyrobase
test ! -d pyrobase || ( cd pyrobase && ../bin/paver -q develop -U)


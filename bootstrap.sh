# This script has to be sourced in a shell and is thus NOT executable.
test ! -f ./bin/activate || return 0
deactivate 2>/dev/null || true
virtualenv --no-site-packages . || return 1

export DEBFULLNAME=pyroscope
export DEBEMAIL=pyroscope.project@gmail.com

cat >>bin/activate <<EOF
export DEBFULLNAME=$DEBFULLNAME
export DEBEMAIL=$DEBEMAIL
EOF

. bin/activate || return 1

# tools
easy_install -U "setuptools==0.6c11" || return 1
easy_install -U "paver>=1.0.1" || return 1
easy_install -U "nose>=1.0" || return 1
easy_install -U "coverage>=3.4" || return 1
easy_install -U "yolk>=0.4.1" || return 1
##easy_install -U "PasteScript>=1.7.3" || return 1

# pyrobase
test ! -d pyrobase || ( cd pyrobase && paver develop -U)


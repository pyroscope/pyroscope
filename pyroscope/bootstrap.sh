# This script has to be sourced in a shell and is thus NOT executable.
virtualenv --no-site-packages . || exit 1
. bin/activate

# tools
easy_install -U "setuptools==0.6c9"
easy_install -U "paver>=1.0.1"
easy_install -U "epydoc>=3.0.1"
easy_install -U "nose>=0.10.3"
easy_install -U "coverage==2.80"
easy_install -U "pylint>=0.18.0"
easy_install -U "yolk>=0.4.1"
easy_install -U "PasteScript>=1.7.3"

# project
paver develop -U
paver bootstrap

export DEBFULLNAME=pyroscope
export DEBEMAIL=pyroscope.project@gmail.com

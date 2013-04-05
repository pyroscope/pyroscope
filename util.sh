# library of helper functions (needs to be sourced)

PROJECT_ROOT=$(cd $(dirname "$0") && pwd)

abend() {
    echo
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo -n >&2 "ERROR: "
    for i in "$@"; do
        echo >&2 "$i"
    done
    set +e
    return 1
}

fail() {
    abend "$@"
    exit 1
}

fix_wrappers() {
    # Ensure unversioned wrappers exist
    for i in "$PROJECT_ROOT"/bin/*-2.*; do
        tool=${i%-*}
        test -x "$tool" || ln -s $(basename "$i") "$tool"
    done
}

ensure_pip() {
    test -x "$PROJECT_ROOT"/bin/pip || "$PROJECT_ROOT"/bin/easy_install -q pip
    test -x "$PROJECT_ROOT"/bin/pip || fix_wrappers
    test -x "$PROJECT_ROOT"/bin/pip || abend "installing pip into $PROJECT_ROOT failed"
}

install_venv() {
    venv='https://github.com/pypa/virtualenv/raw/master/virtualenv.py'
    $PYTHON -c "import urllib2; open('$PROJECT_ROOT/virtualenv.py','w').write(urllib2.urlopen('$venv').read())"
    deactivate 2>/dev/null || true
    $PYTHON "$PROJECT_ROOT"/virtualenv.py "$@" "$PROJECT_ROOT"
    test -f "$PROJECT_ROOT"/bin/activate || abend "creating venv in $PROJECT_ROOT failed"
    rm "$PROJECT_ROOT"/virtualenv.py*

    ensure_pip
}

pip_install_opt() {
    ensure_pip
    "$PROJECT_ROOT"/bin/pip install "$@"
    fix_wrappers
}

pip_install() {
    ensure_pip
    "$PROJECT_ROOT"/bin/pip install "$@" || abend "'pip install $@' failed"
    fix_wrappers
}


See also RtControlExamples and RtXmlRpcReference.

*Contents*

Querying system information
===========================

The ``rtuptime`` script shows you essential information about your
rTorrent instance: \`\`\` #! /bin/bash
SCGI\_SOCKET=~/rtorrent/.scgi\_local

if test ! -S $SCGI\_SOCKET; then echo >&2 "rTorrent is not running (no
socket $SCGI\_SOCKET)" exit 1 fi

echo -n rTorrent :math:`(rtxmlrpc system.client_version)/`\ (rtxmlrpc
system.library\_version) echo -n , up $(rtxmlrpc to\_elapsed\_time $(ls
-l --time-style '+%s' $SCGI\_SOCKET \| awk '{print
:math:`6}')) echo -n \ [`\ (rtcontrol -qosize \* \| awk '{ SUM +=
:math:`1} END { print SUM/1024/1024/1024 }') GiB loaded] echo -n , D:`\ (rtxmlrpc
to\_mb $(rtxmlrpc get\_down\_total)) MiB echo -n  @ $(rtxmlrpc to\_kb
$(rtxmlrpc get\_down\_rate)) echo -n  / $(rtxmlrpc to\_kb
:math:`(rtxmlrpc get_download_rate)) KiB/s echo -n , U:`\ (rtxmlrpc
to\_mb $(rtxmlrpc get\_up\_total)) MiB echo -n  @ $(rtxmlrpc to\_kb
$(rtxmlrpc get\_up\_rate)) echo -n  / $(rtxmlrpc to\_kb $(rtxmlrpc
get\_upload\_rate)) KiB/s echo \`\`\`

When called, it prints something like this:
``$ rtuptime rTorrent 0.8.6/0.12.6, up 24:49:38 [123.456 GiB loaded], D: 42,3 MiB @ 0,1 / 666,0 KiB/s, U: 42,2 MiB @ 42,1 / 42,2 KiB/s``
And yes, doing the same in a `Python script <WriteYourOwnScripts.md>`_
would be much more CPU efficient. ;)

If you connect via ``scgi_port``, touch a file in ``/tmp`` in your
startup script and use that for uptime checking.

General maintenance tasks
=========================

Here are some commands that can help with managing your rTorrent
instance:
``# Flush ALL session data NOW, use this before you make a backup of your session directory rtxmlrpc session_save``

Setting and checking throttles
==============================

To set the speed of the ``slow`` throttle, and then check your new limit
and print the current download rate, use:
``rtxmlrpc throttle_down slow 120 # 0 rtxmlrpc get_throttle_down_max slow  # 122880 rtxmlrpc get_throttle_down_rate slow  # 0``
Note that the speed is specified in KiB/s as a string when setting it
but returned in bytes/s as an integer on queries.

The following script makes this available in an easy usable form, e.g.
"``throttle slow 42``" — it also shows the current rate and settings of
all defined throttles when called without arguments: \`\`\` #! /bin/bash
# Set speed of named throttle

CONFIGURATION
=============

throttle\_name="seed" # default name unit=1024 # KiB/s

HERE BE DRAGONS!
================

down=false if test "$1" = "-d"; then down=true shift fi

if test -n "$(echo $1 \| tr -d 0-9)"; then # Non-numeric $1 is a name
throttle\_name=$1 shift fi

if test -z "$1"; then echo >&2 "Usage: :math:`{0/`\ HOME/~} [-d] [] "

::

    rtorrent_rc=~/.rtorrent.rc
    test -e "$rtorrent_rc" || rtorrent_rc="$(rtxmlrpc system.get_cwd)/rtorrent.rc"
    if test -e "$rtorrent_rc"; then
        throttles="$(egrep '^throttle[._](up|down)' $rtorrent_rc | tr ._=, ' ' | cut -f3 -d" " | sort | uniq)"
        echo
        echo "CURRENT THROTTLE SETTINGS"
        for throttle in $throttles; do
            echo -e "  $throttle\t" \
                "U: $(rtxmlrpc to_kb $(rtxmlrpc get_throttle_up_rate $throttle)) /" \
                "$(rtxmlrpc to_kb $(rtxmlrpc get_throttle_up_max $throttle | sed 's/^-1$/0/')) KiB/s\t" \
                "D: $(rtxmlrpc to_kb $(rtxmlrpc get_throttle_down_rate $throttle)) /" \
                "$(rtxmlrpc to_kb $(rtxmlrpc get_throttle_down_max $throttle | sed 's/^-1$/0/')) KiB/s"
        done
    fi
    exit 2

fi

rate=$(( $1 \* $unit ))

Set chosen bandwidth
====================

if $down; then if test $(rtxmlrpc get\_throttle\_down\_max
$throttle\_name) -ne $rate; then rtxmlrpc -q throttle\_down
$throttle\_name $(( :math:`rate / 1024 )) echo "Throttle '`\ throttle\_name'
download rate changed to"
 "$(( $(rtxmlrpc get\_throttle\_down\_max $throttle\_name) / 1024 ))
KiB/s" fi else if test $(rtxmlrpc get\_throttle\_up\_max
$throttle\_name) -ne $rate; then rtxmlrpc -q throttle\_up
$throttle\_name $(( :math:`rate / 1024 )) echo "Throttle '`\ throttle\_name'
upload rate changed to"
 "$(( $(rtxmlrpc get\_throttle\_up\_max $throttle\_name) / 1024 ))
KiB/s" fi fi \`\`\`

Global throttling when other computers are up
=============================================

If you want to be loved by your house-mates, try this: \`\`\` #!
/bin/bash # Throttle bittorrent when certain hosts are up

CONFIGURATION
=============

hosts\_to\_check="${1:-mom dad}" full\_up=62 full\_down=620 nice\_up=42
nice\_down=123 unit=1024 # KiB/s

HERE BE DRAGONS!
================

Check if any prioritized hosts are up
=====================================

up=$(( $full\_up \* :math:`unit )) down=`\ (( $full\_down \* $unit ))
hosts=""

for host in $hosts\_to\_check; do if ping -c1
:math:`host >/dev/null 2>&1; then up=`\ (( $nice\_up \*
:math:`unit )) down=`\ (( $nice\_down \* :math:`unit )) hosts="`\ hosts
$host" fi done

reason="at full throttle" test -z ":math:`hosts" || reason="for`\ hosts"

Set chosen bandwidth
====================

if test $(rtxmlrpc get\_upload\_rate) -ne $up; then echo "Setting upload
rate to $(( $up / 1024 )) KiB/s $reason" rtxmlrpc -q set\_upload\_rate
$up fi if test $(rtxmlrpc get\_download\_rate) -ne $down; then echo
"Setting download rate to $(( $down / 1024 )) KiB/s $reason" rtxmlrpc -q
set\_download\_rate $down fi \`\`\` Add it to your crontab and run it
every few minutes.

Throttling rTorrent for a limited time
======================================

If you want to slow down rTorrent to use your available bandwidth on
foreground tasks like browsing, but usually forget to return the
throttle settings back to normal, then you can use the provided
`rt-backseat <http://pyroscope.googlecode.com/svn/trunk/pyrocore/docs/examples/rt-backseat>`_
script. It will register a job via ``at``, so that command must be
installed on the machine for it to work. The default throttle speed and
timeout can be set at the top of the script.

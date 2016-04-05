

# Introduction #
The queue manager, and other background jobs you can activate, are controlled by the `pyrotorque` daemon command.

<table border='3'><tr><td>
<b>❢YOU NEED TO RUN SVN HEAD FOR THIS! See InstallFromSource❢</b>
</td></tr></table><br />


# Initial setup #

Before you start configuring the daemon, you have to InstallFromSource the system (if you didn't do that already), **and** some additional Python dependencies it needs to do its work, also depending on what jobs you activate in your configuration. You need at least `APScheduler>=2.0.2`, and the following is how to install the _full_ set of dependencies:
```
~/lib/pyroscope/bin/pip install -r ~/lib/pyroscope/requirements-torque.txt
```

The queue manager daemon needs additional settings, but there are defaults in place, so the detailed explanation in this section can be skipped, if you are OK with these. Go directly to the [configuration](#Configuration.md) in that case.

**➽ IMPORTANT: Remember to follow the [migration guide](MigrationGuide#Migrating_to_version_0.4.3.md) in case you're upgrading an existing installation.**

If you followed the UserConfiguration instructions, the necessary commands are added automatically to your `.rtorrent.rc` using the [configuration include](https://pyroscope.googlecode.com/svn/trunk/pyrocore/src/pyrocore/data/config/rtorrent-0.8.6.rc). Look for the sections starting with a `# TORQUE` comment near the end, if for whatever reason you need to add these manually.

The daemon itself is configured by an additional configuration file `~/.pyroscope/torque.ini` containing the `[TORQUE]` section. Again, this is covered by [defaults](https://pyroscope.googlecode.com/svn/trunk/pyrocore/src/pyrocore/data/config/torque.ini), so you only need to take care of that if you want to make any changes.


# Configuration #

The following is a **minimal `~/.pyroscope/torque.ini` configuration example**, only changing a few values from the defaults:
```
# "pyrotorque" configuration file
#
# For details, see http://code.google.com/p/pyroscope/wiki/QueueManager#Configuration
#

[TORQUE]
# Queue manager
job.queue.active            = True
job.queue.downloading_max   = 3
job.queue.startable         = is_ignored=0 message= prio>0 
        [ NOT [ traits=audio kind_25=jpg,png,tif,bmp ] ]

# Tree watch (works together with the queue)
job.treewatch.active        = True
job.treewatch.load_mode     = start
job.treewatch.queued        = True
job.treewatch.path          = /var/torrent/watch
job.treewatch.cmd.jpg       = f.multicall=*.jpg,f.set_priority=2
job.treewatch.cmd.png       = f.multicall=*.png,f.set_priority=2
job.treewatch.cmd.tif       = f.multicall=*.tif,f.set_priority=0
job.treewatch.cmd.target    = {{# set target path
    }}d.custom.set=targetdir,/var/torrent/done/{{label}}/{{relpath}}
```
Having a minimal configuration with just your changes is recommended, so you get new defaults in later releases automatically.

Note that in the above example for the `queue` job, `downloading_max` counts started-but-incomplete items including those that ignore commands.
Other queue parameters are the minimum number of items in 'downloading' state (`downloading_min`, which trumps `start_at_once`), and the maximum number of items to start in one run (`start_at_once`).
And the `startable` condition adds the extra hurdle that audio downloads that don't stay below a 25% threshold regarding contained images are **not** started automatically — go do that with a plain rTorrent watch dir.

In the `treewatch` job, the "`cmd.«name»`" settings can be used to provide additional load commands, executed during loading the new item, _before_ it is started (in case it is started at all). They're added in the alphabetic order of their names. The above example shows how to set any JPG and PNG images to high priority, and prevent downloading any TIF images by default. Commands can be templates, see TreeWatchExamples for further details.

See the [default configuration](https://pyroscope.googlecode.com/svn/trunk/pyrocore/src/pyrocore/data/config/torque.ini) for **more parameters and what they mean**.


After having completed your configuration, you're ready to **test it, by following these steps**:
  1. Execute `rm ~/.pyroscope/run/pyrotorque` to **prevent the watchdog from starting the manager** in the background.
  1. **Stop any running daemon** process using `pyrotorque --stop`, just in case.
  1. Run `pyrotorque --fg -v` in a terminal, this will **start the job scheduler in the foreground** with verbose logging directly to that terminal, exactly what you need to check out if your configuration does what you intended. It also helps you to understand what goes on "under the hood".
  1. If you applied **changes to your configuration**, stop the running scheduler by pressing CTRL-C, then **restart it**. Wash, rinse, repeat.
  1. Press CTRL-C for the last time and call `pyrotorque --status`, it should show that no daemon process is running.
  1. Execute `touch ~/.pyroscope/run/pyrotorque` — this does **create the guard file again**, which must always exist if you want `pyrotorque` to run in the background (otherwise you'll just get an error message on the console or in the log, if you try to launch it).
  1. **Wait up to 300 seconds**, and if your configuration has the `pyro_watchdog` schedule as it should by now, `pyrotorque --status` will show that a daemon process was automatically started by rTorrent.
  1. Enjoy, and **check `~/.pyroscope/log/torque.log`** for feedback from the daemon process.

If you want to restart the daemon running in the background immediately, e.g. to **reload `torque.ini`** or after a software update, use **`pyrotorque --cron --restart`**.


# Built-in jobs #
The `QueueManager` is just one kind of job that can be run by `pyrotorque`. It has an embedded scheduler that can run any number of additional jobs, the following sections explain the built-in ones. Since these jobs can be loaded from any available Python package, you can also easily [write your own](#Writing_custom_jobs.md).

Jobs and their configuration are added in the `[TORQUE]` section, by providing at least the parameters `job.«NAME».handler` and `job.«NAME».schedule`. Depending on the handler, additional parameters can/must be provided (see below for a list of handlers and what they do).

Details on the `schedule` parameter can be found [here](http://readthedocs.org/docs/apscheduler/en/latest/cronschedule.html). Multiple fields must be separated by spaces, so if a field value contains a space, it must be quoted, e.g. «`hour=12 "day=3rd sun"`».
The `handler` parameter tells the system where to look for the job implementation, see the handler descriptions below for the correct values.

## `QueueManager` ##
`pyrocore.torrent.queue:QueueManager` manages queued downloads (i.e. starts them in a controlled manner), it is described in detail [further up on this page](#Configuration.md).


## `TreeWatch` (beta, not feature-complete) ##
`pyrocore.torrent.watch:TreeWatch` watches a folder tree, which can be nested arbitrarily. Loading of new `.torrent` files is immediate (using `libnotify`).

**TODO** Each sub-directory can contain a `watch.ini` configuration file for parameters like whether to start new items immediately, and for overriding the completion path.

See TreeWatchExamples for further details and sample configurations.


## `EngineStats` ##
`pyrocore.torrent.jobs:EngineStats` runs once per minute, checks the connection to rTorrent, and logs some statistical information.

You can change it to run only hourly by adding this to the configuration:
```
job.connstats.schedule      = hour=*
```


## `ExecCommand` (planned) ##
**TODO** `pyrocore.torrent.jobs:ExecCommand` runs an external command in a shell, i.e. it simply runs cron jobs. The reasons for not using cron instead are these:
  1. You can have all your rTorrent-related background processing at one place, and the commands see the same environment as `pyrotorque`.
  1. `pyrotorque` offers more flexible scheduling, including the ability to run jobs at sub-minute intervals.


## `RemoteWatch` (planned) ##
**TODO** `pyrocore.torrent.watch:RemoteWatch` polls a (S)FTP source for new `.torrent` files, creates a local copy, and loads that into the client.


## `ItemPoller` (planned) ##
**TODO** `pyrocore.torrent.:` maintains an updated copy of all rTorrent items, as a service for the other jobs.


## `ActionRule` (planned) ##
**TODO** `pyrocore.torrent.filter:ActionRule` is `rtcontrol` in form of a house-keeping job, and using this is way more efficient than an equivalent `rtcontrol` cron job; due to that, they can be run a lot more frequently.


## `TorrentMirror` (planned) ##
**TODO** `pyrocore.torrent.filter:TorrentMirror` allows you to transfer a torrent's data from the local client to other remote clients using a specified tracker (at the start, a locally running "bttrack"). In a nutshell, it allows you to transfer any filtered item automatically to a remote location via bittorrent.


## `CompletionHandler` (planned) ##
**TODO** `pyrocore.torrent.:` moves completed data to a target directory, according to flexible rules.


## `StatsArchiver` (planned) ##
**TODO**  `pyrocore.torrent.:` keeps a continuous archive of some statistical values (like bandwidth) so they can later be rendered into graphs.

See RtorrentMonitoring for more details.

## `...` ##
**TODO**  `pyrocore.torrent.:` ...


# Writing custom jobs #
**TODO**

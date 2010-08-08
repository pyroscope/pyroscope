## This is the default HTML page layout
<%!
    page_title = lambda: "*** PAGE TITLE NOT SET ***"
    page_head = lambda: ""
    page_help = lambda: ""
%>
<html>
##  HTML head
    <head>
        <title>${self.attr.page_title()} - PyroScope</title>
        <%include file="/common/yui.mako"/>

        <link rel="stylesheet" type="text/css" charset="utf-8" media="all" href="/css/default.css">
        <script type="text/javascript" src="/js/ps/core.js"></script>
        ${self.attr.page_head()|n}

        <!- Register global events -->
        <script>
            var _timezone = "${c._timezone}";
            stats_activate();
        </script>
    </head>

    <body><div id="doc3" class="yui-skin-sam yui-t5">
    <div id="hd" class="rounded"><!-- header -->
##  Logo
        <div class="logo"><a href="http://pyroscope.googlecode.com/">
            <img src="/img/png/150/logo.png" width="150" height="150" /></a></div>
            ##<img src="/img/png/200x100/logo-wide.png" width="200" height="100" /></a></div>
##  Search box & stats
        <div class="topstats">
            <span>
                ${"console.16 ENGINE ID"|h.icon} ${g.engine_id}
                % if c.engine.startup:
                    started ${c.engine.startup}
                %endif
                % if g.xmlrpc_bug:
                    ${"bio-hazard.16 Your rTorrent installation has the XMLRPC bug!"|h.icon}
                % endif

            </span>
          ##XXX Do this by CSS!
          <br />
            <span>
                <img id="clock_img" src="/img/png/16/clock_red.png" width="16" height="16" title="TIME" />
                <span id="clock">${h.now()}</span>
            </span>
            <span>
                ${"up_rate.16 RATE UP"|h.icon}
                <span class="statsval" id="engine_up_rate">?</span>
                / ${c.engine.max_up_rate|h.bibyte}
            </span>
            <span>
                ${"down_rate.16 RATE DOWN"|h.icon}
                <span class="statsval" id="engine_down_rate">?</span> 
                / ${c.engine.max_down_rate|h.bibyte}
            </span>
          ##XXX Do this by CSS!
          <br />
            <span>
                ${"up_slots.16 SLOTS UP"|h.icon} 
                <span class="statsval" id="engine_up_slots">?</span> 
                / ${c.engine.max_up_slots}
            </span>
            <span>
                ${"down_slots.16 SLOTS DOWN"|h.icon}
                <span class="statsval" id="engine_down_slots">?</span>
                / ${c.engine.max_down_slots}
            </span>
            <span>
                ${"http.16 HTTP"|h.icon}
                <span class="statsval" id="engine_http">?</span>
                / ${c.engine.max_http}
            </span>
            <span>
                ${"socket.16 SOCKETS"|h.icon}
                <span class="statsval" id="engine_sockets">?</span>
                / ${c.engine.max_sockets}
            </span>
            <span>
                ${"storage.16 FILES"|h.icon}
                <span class="statsval" id="engine_files">?</span>
                / ${c.engine.max_files}
            </span>
            <span>
                ${"memory.16 MEMORY"|h.icon}
                <span class="statsval" id="engine_mem">?</span>
                / ${c.engine.max_mem|h.bibyte}
            </span>
            <span>
                <img id="dht_active" src="/img/png/16/network_red.png" width="16" height="16" title="DHT?" />
                <span class="statsval" id="engine_dht">?</span>
                [${c.engine.dht_port}]
            </span>
            <span id="search">
                <form method="GET" action="${h.url_for(controller='search')}">
                  <input type="image" src="/img/png/16/search.png" width="16" height="16" />
                  <input type="text" id="search" name="query" 
                         onfocus="if (this.value == 'Search...') this.value='';" 
                         onblur="if (this.value == '') this.value='Search...';" 
                         value="Search..." size="25" autocomplete="off" />
                </form>
            </span>
        </div>
##  Top-level menu
        <div class="topmenu">
            <ul>
                <li><a id="topmenu-current" href="/index">${"home.24"|h.icon} Home</a></li>
                <li><a href="/view">${"torrent.24"|h.icon} Torrents</a></li>
                <li><a href="/stats">${"chart2.24"|h.icon} Stats</a></li>
                <li><a href="/admin">${"wrench.24"|h.icon} Admin</a></li>
                <li><a href="/sandbox">${"flask.24"|h.icon} Lab</a></li>
                % if self.attr.page_help():
                    <li><a href="/help/wiki/${self.attr.page_help()|u}">${"help.24"|h.icon} Help</a></li>
                % else:
                    <li><a href="/help">${"help.24"|h.icon}Index</a></li>
                % endif
            </ul>
        </div>
        <noscript>
            <strong>Please enable Javascript in your browser to be able to use most features. Thank you.</strong>
        </noscript>
    </div>
##
% for line in c._debug:
    ${line}<br />
% endfor
% if c._messages:
    <div class="messages">
        <ul class="rounded">
            % for msg in c._messages:
            <li>${msg}</li>
            % endfor
        </ul>
    </div>
% endif
##
##  Body of derived template(s)
    <div id="bd"><!-- body -->
        ${next.body()}
    </div>
##  Footer
    <div id="ft" class="rounded"><!-- footer -->
        <small><strong><em>Powered by</em></strong></small>
        &#160; <a href="http://www.python.org/">${"python.png Python_Powered 42x40"|h.img}</a>
        &#160; <a href="http://pylonshq.com/">${"pylons.png Pylons_Powered 59x40"|h.img}</a>
        &#160; <a href="http://www.linux.org/">${"tux.png GNU/Linux_Powered 40x40"|h.img}</a>
        &#160; <a href="http://www.blueskyonmars.com/projects/paver/">${"paver.png Paver_Powered 76x40"|h.img}</a>
        &#160; <a href="http://www.w3.org/Graphics/SVG/">${"svg.png SVG_Powered 40x40"|h.img}</a>
        &#160; <a href="http://developer.yahoo.com/yui/">${"yui.png YUI_Powered 120x37"|h.img}</a>
        &#160; <a href="http://en.wikipedia.org/wiki/Caffeine">${"coffee.png Caffeine_Powered 74x40"|h.img}</a>

        &#160; <span class="bugreport">
            ${"bug.24"|h.icon} <a class="hoverline" href="http://code.google.com/p/pyroscope/issues/entry">Report Bug</a>
        </span>
        &#160; <span class="profilingstats">Page rendered in <!-- LATENCY_PROFILING_RESULT -->.</span>
    </div>

    ## end of YUI body
    </div></body>
</html>

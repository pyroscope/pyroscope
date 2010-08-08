<%doc>
    PAGE: Torrent Views
</%doc>
<%inherit file="/common/pageframe.mako"/>
<%!
    from pylons import tmpl_context as c
    from pyroscope.lib import helpers as h

    echo = lambda url: h.echo(url, ("refresh", "filter", "filter_mode",))

    # Overloaded attributes of pageframe
    page_title = lambda: "Torrents"
    page_help = lambda: "TorrentsView"
    page_head = lambda: '<meta http-equiv="refresh" content="%s" />' % c.refresh_rate
%>
##
## VIEW SELECTION
##
<div class="tab-bar">
<ul>
% for view in c.views:
    <li ${'class="selected"' if view is c.view else "" | n}>
        <a href="${h.url_for(action='list', id=view.action)|echo}">
% if "icon" in view:
            ${view.icon|h.icon}
% endif
            ${view.title}
            ## ${"(%d)" % len(c.torrents) if view is c.view else ""}
        </a>
    </li>
% endfor
</ul>
</div>

##
## TORRENT LIST
##
<div class="tab-box">
    ## FILTER
    <div class="filter">
        <form method="GET" action="">
            ${h.echo('', form=1)}
% if c.filter:
            <a href="?"><img src="/img/png/16/filter-off.png" width="16" height="16" title="Clear filter" /></a>
% endif
            <input type="image" src="/img/png/16/filter.png" width="16" height="16"
                 title="Enter filter glob pattern; syntax: * ? [seq] [!seq]" />
            <input type="text" id="search" name="filter" 
                 onfocus="if (this.value == 'Filter...') this.value='';" 
                 onblur="if (this.value == '') this.value='Filter...';" 
                 value="${c.filter or 'Filter...'}" size="25" autocomplete="off" />
            <input type="radio" name="filter_mode" id="filter-and" value="AND"
                ${'checked="checked"' if c.filter_mode == "AND" else ''} />
            <label for="filter-and">AND</label>
            <input type="radio" name="filter_mode" id="filter-or"  value="OR"
                ${'checked="checked"' if c.filter_mode == "OR" else ''} />
            <label for="filter-or">OR</label>
        </form>
    </div>
    ## BOX TITLE
    <h3>
        ${len(c.torrents)} ${c.view.title} Torrent(s)
% if c.filter:
        ${'[filtered by "%s" out of %d]' % ((' %s ' % c.filter_mode).join(c.filter.split()), c.torrents_unfiltered)}
        <a href="${'?'|h.echo}"><img src="/img/png/12/filter-off.png" width="12" height="12" title="Clear filter" /></a>
% endif
% if c.messages:
        <a href="#messages">
            ${'info_red.16 There are %d tracker message(s)' % len(c.messages)|h.icon}
        </a>
% endif
    </h3>
    <%include file="/views/torrents-list.mako"/>
</div>

##            print "  [%d torrents on %d trackers with %.3f total ratio]" % (
##                len(self.torrents), len(domains),
##               sum(ratios) / 1000.0 / len(ratios),
##            )
##            print "  [%d^v / %d^ / %dv, %d open, %d complete, %d initial seeds]" % (
##                len(active_both), len(active_up), len(active_down),
##                counts["is_open"],
##                counts["complete"],
##                len(seeds),
##            )

##
## MESSAGES
##
% if c.messages:
<div class="tab-box">
<a name="messages">
    <h3>${len(c.messages)} Tracker Message(s)</h3>
</a>

<table class="grid">
    <tr class="header">
        <th class="wide">${"torrent.16"|h.icon} TORRENT</th>
        <th class="wide">${"info_red.16"|h.icon} MESSAGE</th>
        <th class="wide">${"tracker.16"|h.icon} TRACKER</th>
    </tr>
% for idx, item in enumerate(c.messages):
    <tr class="${'odd' if idx&1 else 'even'}">
        <td><a class="tlink" href="${h.url_for(controller='torrent', id=item.hash)}" title="${item.tooltip}">
            ${item.name|h.nostrip,h.obfuscate}
        </a></td>
        <td>${item.text}</td>
        <td>${item.domains|h.obfuscate}</td>
    </tr>
% endfor
</table>
</div>
% endif


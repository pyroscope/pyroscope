<%inherit file="/common/pageframe.mako"/>
<%!
    from cgi import escape
    from pprint import pformat
    from pylons import request, config
    from pylons import tmpl_context as c
    from pyroscope.web.lib import helpers as h

    page_title = lambda: "Laboratory"
    page_help = lambda: "LaboratoryView"
    page_head = lambda: """
        <script src="http://static.simile.mit.edu/timeline/api-2.3.0/timeline-api.js?bundle=true" type="text/javascript"></script>

        <!--[if IE]>  
        <script type="text/javascript" src="/js/jit/excanvas.js"></script>  
        <![endif]-->  
        <script type="text/javascript" src="/js/jit/jit.js" ></script>  
    """

    sizes = (12, 16, 24, 32, 48)

    request_attrs = (
        "params", "environ", "headers", "cookies",
        "host", "scheme", "script_name", "path_info", "method",
    )
%>

<h1>PyroScope Labs</h1>
<div><em>Testing area, enter at your own risk!</em></div>

##
## VIEW SELECTION
##
<div class="tab-bar">
<ul>
% for view, title in sorted(c.views.items()):
    <li ${'class="selected"' if view == c.view else "" | n}>
        <a href="${h.url_for(id=view)|h.echo}">${title}</a>
    </li>
% endfor
</ul>
</div>

<div class="tab-box">
##
## YUI VIEW
##
% if c.view == "yui":
    <div style="background-color: gray">
        <div id="texttipped">Tooltip Test</div>
        <img id="tooltipped" src="/img/png/24/logo.png" /> 

        <span id="mycheckbox" class="yui-button"> 
            <span class="first-child"> 
                <button type="button">Check me!</button> 
            </span> 
        </span> 
        
        <div id="calendar"></div>

        <script type="text/javascript">

            myTooltip = new YAHOO.widget.Tooltip("tt-id", {
                context: "tooltipped",
                text: "You have hovered over Tooltip Test.",
                showDelay: 500
            }); 
            new YAHOO.widget.Tooltip("tt-id2", {
                context: "texttipped",
                text: "You have hovered over a text.",
                showDelay: 500
            }); 

            // A DIV with id "cal1Container" should already exist on the page
            var calendar = new YAHOO.widget.Calendar("calendar");
            calendar.render();

            var oButton = new YAHOO.widget.Button("mycheckbox", { 
                    type: "checkbox", 
                    name: "field1",
                    value: "somevalue"
                }
            );

        </script>
    </div>
% endif

##
## OHLOH VIEW
##
% if c.view == "ohloh":
    <div class="ohloh-widgets">
        % for stats in ("basic_stats", "factoids", "cocomo", "languages", ):
            <div>
                <script type="text/javascript" src="http://www.ohloh.net/p/346666/widgets/project_${stats}.js"></script>
            </div>
        % endfor
    </div>
% endif

##
## ICONS VIEW
##
% if c.view == "icons":
<h3>Sizes [${", ".join("%dx%d" % (sz, sz) for sz in sizes)}]</h3>
% for icon in c.icons:
    <div class="iconbox">
        <div>
            % for size in sizes:
                ${"%s.%d" % (icon, size)|h.icon}
            % endfor
        </div>
        <div>${icon}</div>
    </div>
% endfor
    <!-- end icon float -->
    <div style="clear:both;"></div>
</div>
% endif

##
## GLOBALS VIEW
##
% if c.view == "globals":
##${repr(g)}
<h3>Globals</h3>
<dl style="margin-left: 0;">
% for k, v in sorted(g.items()):
  % if not k.startswith('_'):
    <dt>${k}</dt>
    <dd><code>${repr(g[k] or "N/A")}</code></dd>
  % endif
% endfor
</dl>
<h3>Config</h3>
##${repr(config)}
<dl style="margin-left: 0;">
% for k, v in sorted(config.items()):
  <dt>${k}</dt>
  <dd><code>
  % if isinstance(getattr(config, k, None), (dict, list, tuple)):
    ${'<br />'.join(escape(pformat(config[k])).replace(' ', '&#160;').splitlines())|n}
  % else:
    ${repr(config.get(k, "N/A"))}
  % endif
  </code></dd>
% endfor
</dl>
% endif

##
## REQUEST VIEW
##
% if c.view == "request":
${repr(request)}
<dl style="margin-left: 0;">
% for k in request_attrs:
  <dt>
    ${k} ${repr(type(getattr(request, k, None)))}
    ${getattr(getattr(request, k), '__module__', '')}
  </dt>
  <dd><code>
  ##% if type(getattr(request, k, None)) == dict:
  % if isinstance(getattr(request, k, None), (dict, list, tuple)):
    ${'<br />'.join(escape(pformat(getattr(request, k))).replace(' ', '&#160;').splitlines())|n}
  % else:
    ${repr(getattr(request, k, "N/A"))}
  % endif
</code></dd>
% endfor
</dl>
% endif

##
## HELPERS VIEW
##
% if c.view == "helpers":
<dl style="margin-left: 0;">
% for k in dir(h):
  %if not k.startswith('_'):
    <dt>${k}</dt><dd><code>${escape(getattr(h, k).__doc__ or "N/A").replace('\n', "<br />")|n}</code></dd>
  % endif
% endfor
</dl>
% endif

##
## JSON VIEW
##
% if c.view == "json":
<dl style="margin-left: 0;">
% for name, docs in sorted(c.json_api.items()):
  <dt><a href="${h.url_for(controller='json', action=name)}">${name}</a></dt><dd>${docs or 'N/A'}</dd>
% endfor
</dl>
% endif

##
## RTORRENT VIEW
##
% if c.view == "rtorrent":
<div>
<a href="?">Default View</a>
| <a href="?methods=1">List Methods</a>
</div>

## ~~~ Methods listing ~~~
% if hasattr(c, "methods"):
    <div>
    % for letter, methods in sorted(c.methods.items()):
        <a href="#${letter}">[${letter}]</a>&nbsp;
    % endfor
    </div>

    % for letter, methods in sorted(c.methods.items()):
        <a name="${letter}"><h5>${letter}</h5></a>
        <div>
        % for method, (signatures, help) in sorted(methods):
            % for signature in signatures:
                <code><strong>${method}</strong>(<em>${', '.join(signature[1:])}</em>)
                </code>&#8658;<code> <em>${signature[0]}</em>
<%!
    def typed_result(method):
        result = getattr(c.proxy.rpc, method)()
        return "%r %r" % (type(result), result)
%>
                % if method in c.rt_globals:
                    <strong>${typed_result(method)}</strong>
                % endif
                </code> ${help}<br />
            % endfor
        % endfor
        </div>
    % endfor

## ~~~ Default ~~~
% else:
##view.size('main') = ${c.proxy.rpc.view.size('main')}<br />
##view.size_not_visible('main') = ${c.proxy.rpc.view.size_not_visible('main')}<br />

% for method in (c.rt_globals):
    ${method} = ${repr(getattr(c.proxy.rpc, method)())}<br />
% endfor

##    ${repr(c.proxy.rpc)}<br />
## ~~~ End rTorrent ~~~
% endif
% endif

##
## TIMELINE VIEW
##
% if c.view == "timeline":
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<h2>Metafile Download Timeline</h2>
<div id="timeline" style="height: 500px; border: 1px solid #aaa"></div>

<script>
var tl;
function time_line() {
    var eventSource = new Timeline.DefaultEventSource();
    var bandInfos = [
        Timeline.createBandInfo({
            eventSource:    eventSource,
            date:           "${c.now}",
            width:          "90%", 
            intervalUnit:   Timeline.DateTime.DAY, 
            intervalPixels: 500
        }),
        Timeline.createBandInfo({
            overview:       true,
            eventSource:    eventSource,
            date:           "${c.now}",
            width:          "10%", 
            intervalUnit:   Timeline.DateTime.MONTH, 
            intervalPixels: 100
        })
    ];
    bandInfos[1].syncWith = 0;
    bandInfos[1].highlight = true;
   
    tl = Timeline.create(document.getElementById("timeline"), bandInfos);
    Timeline.loadXML("${'/sandbox/data/timeline.xml'|h.echo}", function(xml, url) { eventSource.loadXML(xml, url); });
}

YAHOO.util.Event.onDOMReady(time_line);
</script>

##~~~ TIMELINE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% endif

##
## JIT VIEW
##
% if c.view == "jit":
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

<h2>JavaScript InfoVis Toolkit</h2>
<a href="http://thejit.org/">Homepage</a>
|
<select id="tree-switch">
    <option>left</option>
    <option>top</option>
    <option>right</option>
    <option>bottom</option>
</select>

##<div id="st-infovis" class="infovis-root"></div>  
<div id="tm-infovis" class="infovis-root"></div>  
   
<script>

function treeMap(json) {
    //var infovis = document.getElementById('infovis');
    //var w = infovis.offsetWidth, h = infovis.offsetHeight;
    //infovis.style.width = w + 'px';
    //infovis.style.height = h + 'px';

    //var tree = new TM.SliceAndDice({
    //var tree = new TM.Strip({
    var tree = new TM.Squarified({
        // Where to inject the Treemap  
        rootId: 'tm-infovis',

        Color: {
            // Allow coloring
            allow: true,

            // Select a value range for the $color
            // property. Default's to -100 and 100.
            minValue: 0,
            maxValue: 100,

            // Set color range. Default's to reddish and
            // greenish. It takes an array of three
            // integers as R, G and B values.
            minColorValue: [0, 0, 0],
            maxColorValue: [224, 224, 96]
        }
    });  

    // load json data
    tree.loadJSON(json);
}

function spaceTree(json) {
    // Create a new canvas instance.
    var canvas = new Canvas('mycanvas', {
        // Where to inject canvas. Any HTML container will do.
        'injectInto': 'st-infovis',

        // Set width and height, default's to 200.
        'width': 900,
        'height': 500,

        // Set a background color in case the browser
        // does not support clearing a specific area.
        'backgroundColor': '#ffd'
    });

    // Create a new tree instance
    //var tree = new Hypertree(canvas, {
    var tree = new ST(canvas, {
        // set node and edge colors
        Node: {
            color: '#6ff'
        },
        Edge: {
            color: '#33f'
        },

        // Add an event handler to the node when creating it.  
        onCreateLabel: function(label, node) {  
            label.id = node.id;  
            label.innerHTML = node.name;  
            label.onclick = function() {  
                tree.onClick(node.id);  
            };  
        },  
    });

    // load json data
    tree.loadJSON(json);

    // compute node positions and layout
    tree.compute();

    // optional: make a translation of the tree
    //Tree.Geometry.translate(tree.tree, new Complex(-200, 0), "startPos");

    // Emulate a click on the root node.
    tree.onClick(tree.root);

    // Add input handler to switch spacetree orientation.
    var select = document.getElementById('tree-switch');
    select.onchange = function() {
        var index = select.selectedIndex;
        var orientation = select.options[index].text;
        select.disabled = true;
        tree.switchPosition(orientation, {
            onComplete: function() {
                select.disabled = false;
            }
        });
    };
}

function jit_load() {
    var callbacks = {
        // Successful XHR response handler
        success: function(o) {
            var data = [];

            // Use the JSON Utility to parse the data returned from the server
            try {
                data = YAHOO.lang.JSON.parse(o.responseText);
            }
            catch (x) {
                alert("JSON Parse failed (" + x + ") for " + o.responseText + "!");
                return;
            }

            treeMap(data);
            //spaceTree(data);
        }
    };

    // Make the call to the server for JSON data
    YAHOO.util.Connect.asyncRequest('GET', "/sandbox/jit/spacetree.json", callbacks);
};

YAHOO.util.Event.onDOMReady(jit_load);
</script>

##~~~ JIT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% endif

##
## SANDBOX VIEW
##
% if c.view == "sandbox":
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

% endif
## END TAB CONTENT
<div style="clear:both;"></div>
</div>


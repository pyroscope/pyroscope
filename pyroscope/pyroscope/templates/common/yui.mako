<%doc>
    INCLUDE: YUI Loading

</%doc>
<%!
    yui_use_configurator = 0
    yui_dev_tools = 0
%>
% if yui_use_configurator:
## Configurator: combined minified files
## http://developer.yahoo.com/yui/articles/hosting/?base&button&calendar&connection&container&containercore&dom&event&fonts&grids&json&reset&yahoo&MIN
<!-- Combo-handled YUI CSS files: -->
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/combo?2.7.0/build/reset-fonts-grids/reset-fonts-grids.css&2.7.0/build/base/base-min.css&2.7.0/build/assets/skins/sam/skin.css">
<!-- Combo-handled YUI JS files: -->
<script type="text/javascript" src="http://yui.yahooapis.com/combo?2.7.0/build/yahoo-dom-event/yahoo-dom-event.js&2.7.0/build/element/element-min.js&2.7.0/build/button/button-min.js&2.7.0/build/calendar/calendar-min.js&2.7.0/build/connection/connection-min.js&2.7.0/build/container/container-min.js&2.7.0/build/json/json-min.js"></script>

% else:
## Single expanded files
<!--CSS Foundation: (also partially aggegrated in reset-fonts-grids.css; does not include base.css)--> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset/reset-min.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/base/base-min.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/fonts/fonts-min.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/grids/grids-min.css"> 
 
<!--CSS for Controls:--> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/container/assets/skins/sam/container.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/menu/assets/skins/sam/menu.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/autocomplete/assets/skins/sam/autocomplete.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/button/assets/skins/sam/button.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/calendar/assets/skins/sam/calendar.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/carousel/assets/skins/sam/carousel.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/colorpicker/assets/skins/sam/colorpicker.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/datatable/assets/skins/sam/datatable.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/editor/assets/skins/sam/editor.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/imagecropper/assets/skins/sam/imagecropper.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/layout/assets/skins/sam/layout.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/paginator/assets/skins/sam/paginator.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/resize/assets/skins/sam/resize.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/tabview/assets/skins/sam/tabview.css"> 
<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/treeview/assets/skins/sam/treeview.css"> 
 
 
<!--YUI Core (also aggregated in yahoo-dom-event.js; see readmes in the 
YUI download for details on each of the aggregate files and their contents):--> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yahoo/yahoo-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/dom/dom-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/event/event-min.js"></script> 
 
<!--Utilities (also partialy aggregated utilities.js; see readmes in the 
YUI download for details on each of the aggregate files and their contents):--> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/element/element-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/animation/animation-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/connection/connection-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/cookie/cookie-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/datasource/datasource-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/dragdrop/dragdrop-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/get/get-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/history/history-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/imageloader/imageloader-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/json/json-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/resize/resize-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/selector/selector-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yuiloader/yuiloader-min.js"></script> 
 
<!--YUI's UI Controls:--> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/container/container-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/menu/menu-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/autocomplete/autocomplete-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/button/button-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/calendar/calendar-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/charts/charts-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/colorpicker/colorpicker-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/datatable/datatable-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/editor/editor-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/imagecropper/imagecropper-min.js"></script> 
<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/layout/layout-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/paginator/paginator-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/slider/slider-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/tabview/tabview-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/treeview/treeview-min.js"></script> 
##<script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/uploader/uploader-min.js"></script> 

% if yui_dev_tools:
    <!--YUI Developer Tools: Logging, Testing and Profiling --> 
    <!--These are all components that are useful in developing and debugging 
        your work; however, none of these is designed to be a user-facing 
        component.  They are specifically targeted toward easing your work 
        as a developer.--> 
    <!--css--> 
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/logger/assets/skins/sam/logger.css"> 
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/profilerviewer/assets/skins/sam/profilerviewer.css"> 
    <!--js--> 
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/logger/logger-min.js"></script> 
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/profiler/profiler-min.js"></script> 
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/profilerviewer/profilerviewer-min.js"></script> 
    <script type="text/javascript" src="http://yui.yahooapis.com/2.7.0/build/yuitest/yuitest-min.js"></script> 
% endif

##<!--.swf file for the YUI Charts Control--> 
##<script type="text/javascript"> 
##YAHOO.widget.Chart.SWFURL = "http://yui.yahooapis.com/2.7.0/build/charts/assets/charts.swf"; 
##</script>

% endif

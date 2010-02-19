<%inherit file="/common/pageframe.mako"/>
<%!
    from pyroscope.web.lib import helpers as h
    page_title = lambda: "Main Index"
    page_help = lambda: "HomeView"
%>
<%include file="/common/wiki-summary.mako"/>

<h1>Welcome to PyroScope</h1>

<div>For the moment, the 1st rule is <em>functionality over eye candy</em>, 
so expect the latter after there's actually some data to please the eye.</div>

<div><em>
<strong>This is alpha software, expect things (esp. links) to be broken from time to time.</strong>
<br />
Report any bugs to the <a href="http://code.google.com/p/pyroscope/issues/entry">Google Code Issue Tracker</a>.
</em></div>

${c.page.html}


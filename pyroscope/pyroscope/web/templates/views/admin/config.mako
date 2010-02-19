<%doc>
    VIEW: Configuration Files
</%doc>
<%!
    #from pylons import tmpl_context as c
    from pyroscope.web.lib import helpers as h
%>

<h3>${c.filename}</h3>
<code class="listing">
% for line in c.lines:
    ${line}<br />
% endfor
</code>


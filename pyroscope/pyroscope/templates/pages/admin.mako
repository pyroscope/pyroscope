<%doc>
    PAGE: Administration
</%doc>
<%inherit file="/common/pageframe.mako"/>
<%!
    from pylons import tmpl_context as c
    from pyroscope.lib import helpers as h

    # Overloaded attributes of pageframe
    page_title = lambda: "Administration"
    page_help = lambda: "AdminView"
%>
##
## VIEW SELECTION
##
<div class="tab-bar">
<ul>
% for view in c.views:
    <li ${'class="selected"' if view is c.view else "" | n}>
        <a href="${h.url_for(action=view.action, id='')|h.echo}">
            ${view.icon|h.icon}
            ${view.title}
        </a>
    </li>
% endfor
</ul>
</div>

##
## VIEW CONTENTS
##
<div class="tab-box">
% if c.view:
    <%include file="/views/admin/${c.view.action}.mako"/>
% else:
    <div>Please select a view...</div>
% endif
</div>


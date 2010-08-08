<%inherit file="/common/pageframe.mako"/>
<%!
    from pylons import tmpl_context as c

    page_title = lambda: c.page.title
%>
<%include file="/common/wiki-summary.mako"/>

${c.page.html}
##<hr />${repr(c.page.html)}


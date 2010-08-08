<%inherit file="/common/pageframe.mako"/>
<%!
    import time
    from pyroscope.lib import helpers as h
    from pylons import tmpl_context as c

    page_title = lambda: "%s - Torrent View" % h.obfuscate(c.name)

    def ago(t, now=time.time()):
        secs = int(now) - int(t)
        return "%d:%02d:%02d" % (secs // 3600, secs // 60 % 60, secs % 60)
    typeval = lambda val: "%r %r" % (val, type(val))
    sizeval = lambda sz: h.bibyte(sz)
    
    item = c.torrents[0] if c.torrents else None
%>

<h1>Torrent ${c.name|h.obfuscate}</h1>

Hash: <code>${c.hash}</code><br />

% if item:
    ${item.size_bytes} ${item.size_bytes|sizeval}
    <br />
    ${(item.size_chunks-1) * item.chunk_size + item.size_bytes % item.chunk_size}
    ${(item.size_chunks-1) * item.chunk_size + item.size_bytes % item.chunk_size|sizeval}
    ${((item.size_chunks-1) * item.chunk_size + item.size_bytes % item.chunk_size) / 1024.0 / 1024.0}
    <br />

    <br />
    <table>
    <tr><th>base_filename</th><td>${typeval(item.base_filename)}</td></tr>
    <tr><th>base_path</th><td>${typeval(item.base_path)}</td></tr>
    ##<tr><th>bitfield</th><td>${typeval(item.bitfield)}</td></tr>
    <tr><th>bytes_done</th><td>${typeval(item.bytes_done)} &nbsp; ${item.bytes_done|sizeval}</td></tr>
    <tr><th>chunk_size</th><td>${typeval(item.chunk_size)} &nbsp; ${item.chunk_size|sizeval}</td></tr>
    <tr><th>chunks_hashed</th><td>${typeval(item.chunks_hashed)}</td></tr>
    <tr><th>complete</th><td>${typeval(item.complete)}</td></tr>
    <tr><th>completed_bytes</th><td>${typeval(item.completed_bytes)} &nbsp; ${item.completed_bytes|sizeval}</td></tr>
    <tr><th>completed_chunks</th><td>${typeval(item.completed_chunks)}</td></tr>
    <tr><th>connection_current</th><td>${typeval(item.connection_current)}</td></tr>
    <tr><th>connection_leech</th><td>${typeval(item.connection_leech)}</td></tr>
    <tr><th>connection_seed</th><td>${typeval(item.connection_seed)}</td></tr>
    <tr><th>creation_date</th><td>${typeval(item.creation_date)}</td></tr>
    ##<tr><th>custom</th><td>${typeval(item.custom)}</td></tr>
    <tr><th>custom1</th><td>${typeval(item.custom1)}</td></tr>
    <tr><th>custom2</th><td>${typeval(item.custom2)}</td></tr>
    <tr><th>custom3</th><td>${typeval(item.custom3)}</td></tr>
    <tr><th>custom4</th><td>${typeval(item.custom4)}</td></tr>
    <tr><th>custom5</th><td>${typeval(item.custom5)}</td></tr>
    ##<tr><th>custom_throw</th><td>${typeval(item.custom_throw)}</td></tr>
    <tr><th>directory</th><td>${typeval(item.directory)}</td></tr>
    <tr><th>directory_base</th><td>${typeval(item.directory_base)}</td></tr>
    <tr><th>down_rate</th><td>${typeval(item.down_rate)} &nbsp; ${item.down_rate|sizeval}</td></tr>
    <tr><th>down_total</th><td>${typeval(item.down_total)} &nbsp; ${item.down_total|sizeval}</td></tr>
    <tr><th>free_diskspace</th><td>${typeval(item.free_diskspace)} &nbsp; ${item.free_diskspace|sizeval}</td></tr>
    <tr><th>hash</th><td>${typeval(item.hash)}</td></tr>
    <tr><th>hashing</th><td>${typeval(item.hashing)}</td></tr>
    <tr><th>hashing_failed</th><td>${typeval(item.hashing_failed)}</td></tr>
    <tr><th>ignore_commands</th><td>${typeval(item.ignore_commands)}</td></tr>
    <tr><th>left_bytes</th><td>${typeval(item.left_bytes)} &nbsp; ${item.left_bytes|sizeval}</td></tr>
    <tr><th>loaded_file</th><td>${typeval(item.loaded_file)}</td></tr>
    <tr><th>local_id</th><td>${typeval(item.local_id)}</td></tr>
    <tr><th>local_id_html</th><td>${typeval(item.local_id_html)}</td></tr>
    <tr><th>max_file_size</th><td>${typeval(item.max_file_size)}</td></tr>
    <tr><th>max_size_pex</th><td>${typeval(item.max_size_pex)}</td></tr>
    <tr><th>message</th><td>${typeval(item.message)}</td></tr>
    ##<tr><th>mode</th><td>${typeval(item.mode)}</td></tr>
    <tr><th>name</th><td>${typeval(item.name)}</td></tr>
    <tr><th>peer_exchange</th><td>${typeval(item.peer_exchange)}</td></tr>
    <tr><th>peers_accounted</th><td>${typeval(item.peers_accounted)}</td></tr>
    <tr><th>peers_complete</th><td>${typeval(item.peers_complete)}</td></tr>
    <tr><th>peers_connected</th><td>${typeval(item.peers_connected)}</td></tr>
    <tr><th>peers_max</th><td>${typeval(item.peers_max)}</td></tr>
    <tr><th>peers_min</th><td>${typeval(item.peers_min)}</td></tr>
    <tr><th>peers_not_connected</th><td>${typeval(item.peers_not_connected)}</td></tr>
    <tr><th>priority</th><td>${typeval(item.priority)}</td></tr>
    <tr><th>priority_str</th><td>${typeval(item.priority_str)}</td></tr>
    <tr><th>ratio</th><td>${typeval(item.ratio)}</td></tr>
    <tr><th>size_bytes</th><td>${typeval(item.size_bytes)} &nbsp; ${item.size_bytes|sizeval}</td></tr>
    <tr><th>size_chunks</th><td>${typeval(item.size_chunks)}</td></tr>
    <tr><th>size_files</th><td>${typeval(item.size_files)}</td></tr>
    <tr><th>size_pex</th><td>${typeval(item.size_pex)}</td></tr>
    <tr><th>skip_rate</th><td>${typeval(item.skip_rate)}</td></tr>
    <tr><th>skip_total</th><td>${typeval(item.skip_total)}</td></tr>
    <tr><th>state</th><td>${typeval(item.state)}</td></tr>
    <tr><th>state_changed</th><td>${typeval(item.state_changed)}
        &nbsp; ${time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.state_changed))}
        &nbsp; ${item.state_changed|ago}
    </td></tr>
    <tr><th>state_counter</th><td>${typeval(item.state_counter)}</td></tr>
    ##<tr><th>throttle_name</th><td>${typeval(item.throttle_name)}</td></tr>
    <tr><th>tied_to_file</th><td>${typeval(item.tied_to_file)}</td></tr>
    <tr><th>tracker_focus</th><td>${typeval(item.tracker_focus)}</td></tr>
    <tr><th>tracker_numwant</th><td>${typeval(item.tracker_numwant)}</td></tr>
    <tr><th>tracker_size</th><td>${typeval(item.tracker_size)}</td></tr>
    <tr><th>up_rate</th><td>${typeval(item.up_rate)}</td></tr>
    <tr><th>up_total</th><td>${typeval(item.up_total)}</td></tr>
    <tr><th>uploads_max</th><td>${typeval(item.uploads_max)}</td></tr>
    <tr><th>is_active</th><td>${typeval(item.is_active)}</td></tr>
    <tr><th>is_hash_checked</th><td>${typeval(item.is_hash_checked)}</td></tr>
    <tr><th>is_hash_checking</th><td>${typeval(item.is_hash_checking)}</td></tr>
    <tr><th>is_multi_file</th><td>${typeval(item.is_multi_file)}</td></tr>
    <tr><th>is_open</th><td>${typeval(item.is_open)}</td></tr>
    <tr><th>is_pex_active</th><td>${typeval(item.is_pex_active)}</td></tr>
    <tr><th>is_private</th><td>${typeval(item.is_private)}</td></tr>
    </table>
% endif


def iplookup(conn, s):
    import mb.mberr
    from mb.util import IpAddress

    if s[0].isdigit():
        a = IpAddress()
        if ":" in s:
            a.ip6 = s
        else:
            a.ip = s

    else:
        import socket
        import sys

        ips = []
        ip6s = []
        try:
            for res in socket.getaddrinfo(s, None):
                af, socktype, proto, canonname, sa = res
                if ":" in sa[0]:
                    if sa[0] not in ip6s:
                        ip6s.append(sa[0])
                elif sa[0] not in ips:
                    ips.append(sa[0])
        except OSError as e:
            if e[0] == socket.EAI_NONAME:
                raise mb.mberr.NameOrServiceNotKnown(s) from e
            else:
                print("socket error msg:", str(e))
                return None

        # print ips
        # print ip6s
        if len(ips) > 1 or len(ip6s) > 1:
            print(
                ">>> warning: %r resolves to multiple IP addresses: " % s,
                end=" ",
                file=sys.stderr,
            )
            if len(ips) > 1:
                print(", ".join(ips), end=" ", file=sys.stderr)
            if len(ip6s) > 1:
                print(", ".join(ip6s), end=" ", file=sys.stderr)
            print(
                "\n>>> see http://mirrorbrain.org/archive/mirrorbrain/0042.html why\n"
                ">>> this could be a problem, and what to do about it. But note that\n"
                ">>> this is not necessarily a problem and could actually be \n"
                ">>> intended depending on the mirror's configuration (see\n"
                ">>> http://mirrorbrain.org/issues/issue152). It's best to talk to\n"
                ">>> the mirror's admins.\n",
                file=sys.stderr,
            )
        a = IpAddress()
        if ips:
            a.ip = ips[0]
        if ip6s:
            a.ip6 = ip6s[0]

    if not a.ip:
        return a
    query = (
        """SELECT pfx, asn \
                   FROM pfx2asn \
                   WHERE pfx >>= ip4r('%s') \
                   ORDER BY ip4r_size(pfx) \
                   LIMIT 1"""
        % a.ip
    )

    try:
        res = conn.Pfx2asn._connection.queryAll(query)
    except AttributeError:
        # we get this error if mod_asn isn't installed as well
        return a

    if len(res) != 1:
        return a
    (a.prefix, a.asn) = res[0]
    return a


def asn_prefixes(conn, asn):
    query = (
        """SELECT pfx \
                   FROM pfx2asn \
                   WHERE asn='%s'"""
        % asn
    )

    res = conn.Pfx2asn._connection.queryAll(query)
    return [i[0] for i in res]

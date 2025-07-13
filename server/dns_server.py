import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, CNAME
from zone.zone_loader import load_zones

zones = load_zones()

def resolve(query):
    qname = str(query.q.qname)
    qtype = QTYPE[query.q.qtype]
    print(f"Query: {qname} ({qtype})")

    if qname in zones:
        zone = zones[qname]

        # Direct A match
        if qtype == "A":
            if "A" in zone:
                ip = zone["A"]
                ttl = zone.get("TTL", 300)
                return RR(qname, QTYPE.A, rdata=A(ip), ttl=ttl)

            # CNAME fallback
            elif "CNAME" in zone:
                cname = zone["CNAME"]
                cname_rr = RR(qname, QTYPE.CNAME, rdata=CNAME(cname), ttl=zone.get("TTL", 300))

                if cname in zones and "A" in zones[cname]:
                    ip = zones[cname]["A"]
                    a_rr = RR(cname, QTYPE.A, rdata=A(ip), ttl=zones[cname].get("TTL", 300))
                    return [cname_rr, a_rr]
                else:
                    return cname_rr

        # Explicit CNAME query
        elif qtype == "CNAME" and "CNAME" in zone:
            cname = zone["CNAME"]
            return RR(qname, QTYPE.CNAME, rdata=CNAME(cname), ttl=zone.get("TTL", 300))

    return None

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8053))  # You can change port if needed
    print("✅ DNS Server running on 127.0.0.1:8053...")

    while True:
        data, addr = sock.recvfrom(512)
        request = DNSRecord.parse(data)
        reply = request.reply()

        answer = resolve(request)
        if answer:
            if isinstance(answer, list):
                for record in answer:
                    reply.add_answer(record)
            else:
                reply.add_answer(answer)

        sock.sendto(reply.pack(), addr)

if __name__ == "__main__":
    run_server()


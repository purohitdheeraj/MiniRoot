import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, CNAME, NS, SOA, TXT, MX, PTR
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

        # NS (Name Server) records
        elif qtype == "NS" and "NS" in zone:
            ns_servers = zone["NS"]
            if isinstance(ns_servers, list):
                return [RR(qname, QTYPE.NS, rdata=NS(ns), ttl=zone.get("TTL", 300)) for ns in ns_servers]
            else:
                return RR(qname, QTYPE.NS, rdata=NS(ns_servers), ttl=zone.get("TTL", 300))

        # SOA (Start of Authority) records
        elif qtype == "SOA" and "SOA" in zone:
            soa_data = zone["SOA"]
            soa_rr = RR(qname, QTYPE.SOA, rdata=SOA(
                mname=soa_data["mname"],
                rname=soa_data["rname"],
                times=(
                    soa_data["serial"],
                    soa_data["refresh"],
                    soa_data["retry"],
                    soa_data["expire"],
                    soa_data["minimum"]
                )
            ), ttl=zone.get("TTL", 300))
            return soa_rr

        # TXT records
        elif qtype == "TXT" and "TXT" in zone:
            txt_data = zone["TXT"]
            if isinstance(txt_data, list):
                return [RR(qname, QTYPE.TXT, rdata=TXT(txt), ttl=zone.get("TTL", 300)) for txt in txt_data]
            else:
                return RR(qname, QTYPE.TXT, rdata=TXT(txt_data), ttl=zone.get("TTL", 300))

        # MX (Mail Exchange) records
        elif qtype == "MX" and "MX" in zone:
            mx_records = zone["MX"]
            if isinstance(mx_records, list):
                return [RR(qname, QTYPE.MX, rdata=MX(mx["exchange"], mx["priority"]), ttl=zone.get("TTL", 300)) for mx in mx_records]
            else:
                return RR(qname, QTYPE.MX, rdata=MX(mx_records["exchange"], mx_records["priority"]), ttl=zone.get("TTL", 300))

        # PTR (Pointer) records for reverse DNS
        elif qtype == "PTR" and "PTR" in zone:
            ptr_target = zone["PTR"]
            return RR(qname, QTYPE.PTR, rdata=PTR(ptr_target), ttl=zone.get("TTL", 300))

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


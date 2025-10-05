import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, NS

# Root server zone data - simulates the 13 root servers
ROOT_ZONES = {
    "com.": {
        "NS": ["a.gtld-servers.net.", "b.gtld-servers.net.", "c.gtld-servers.net."],
        "A": ["192.5.6.30", "192.33.14.30", "192.26.92.30"]
    },
    "org.": {
        "NS": ["a0.org.afilias-nst.org.", "a2.org.afilias-nst.org.", "c0.org.afilias-nst.info."],
        "A": ["199.19.56.1", "199.19.57.1", "199.19.58.1"]
    },
    "net.": {
        "NS": ["a.gtld-servers.net.", "b.gtld-servers.net.", "c.gtld-servers.net."],
        "A": ["192.5.6.30", "192.33.14.30", "192.26.92.30"]
    },
    "edu.": {
        "NS": ["a.edu-servers.net.", "c.edu-servers.net.", "d.edu-servers.net."],
        "A": ["192.12.94.30", "192.26.92.30", "192.31.80.30"]
    },
    "gov.": {
        "NS": ["a.gov-servers.net.", "b.gov-servers.net.", "c.gov-servers.net."],
        "A": ["192.5.6.30", "192.33.14.30", "192.26.92.30"]
    }
}

def resolve_root_query(domain, qtype):
    """Resolve queries at the root server level"""
    print(f"🌍 Root server query: {domain} ({qtype})")
    
    # For root server, we handle TLD queries directly
    if domain in ROOT_ZONES:
        zone = ROOT_ZONES[domain]
        
        if qtype == "NS":
            # Return NS records for TLD delegation
            reply = DNSRecord.question(domain, "NS").reply()
            for ns in zone["NS"]:
                reply.add_answer(RR(domain, QTYPE.NS, rdata=NS(ns), ttl=3600))
            return reply
        
        elif qtype == "A":
            # Return A records for TLD servers
            reply = DNSRecord.question(domain, "A").reply()
            for ns in zone["NS"]:
                # Get A record for each NS server
                for ip in zone["A"]:
                    reply.add_answer(RR(ns, QTYPE.A, rdata=A(ip), ttl=3600))
            return reply
    
    print(f"❌ No delegation found for {domain}")
    return None

def run_root_server():
    """Run the root DNS server simulator"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8055))  # Port 8055 for root server
    print("🌍 Root DNS Server Simulator running on 127.0.0.1:8055...")
    print("📍 Simulates the 13 root servers")
    print("🔗 Knows about TLD servers (.com, .org, .net, .edu, .gov)")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            
            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]
            
            print(f"\n📨 Root Query: {qname} ({qtype}) from {addr}")
            
            # Try to resolve the query
            response = resolve_root_query(qname, qtype)
            
            if response:
                print(f"✅ Root server response for {qname}")
                sock.sendto(response.pack(), addr)
            else:
                print(f"❌ No delegation found for {qname}")
                reply = request.reply()
                reply.rcode = 3  # NXDOMAIN
                sock.sendto(reply.pack(), addr)
            
        except Exception as e:
            print(f"Error handling root query: {e}")

if __name__ == "__main__":
    run_root_server()

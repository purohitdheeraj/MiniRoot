import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, CNAME
from zone.zone_loader import load_zones

# Load our authoritative zones
zones = load_zones()

def query_external_dns(domain, qtype):
    """Query external DNS server (Google DNS)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        query = DNSRecord.question(domain, qtype)
        sock.sendto(query.pack(), ("8.8.8.8", 53))
        
        data, addr = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        
        sock.close()
        return response
    except Exception as e:
        print(f"Error querying external DNS: {e}")
        return None

def run_final_recursive_server():
    """Run the final recursive DNS server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8054))
    print("✅ Final Recursive DNS Server running on 127.0.0.1:8054...")
    print("🌍 Can resolve both local domains and external domains!")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            
            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]
            
            print(f"\n📨 Query: {qname} ({qtype}) from {addr}")
            
            # Check if we have authoritative data
            if qname in zones and qtype == "A":
                zone = zones[qname]
                if "A" in zone:
                    ip = zone["A"]
                    ttl = zone.get("TTL", 300)
                    
                    # Create reply with correct ID
                    reply = request.reply()
                    reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=ttl))
                    print(f"✅ Authoritative response: {qname} -> {ip}")
                    
                    sock.sendto(reply.pack(), addr)
                    continue
            
            # Try recursive resolution for external domains
            print(f"🔍 Not authoritative, trying recursive resolution for {qname}")
            external_response = query_external_dns(qname, qtype)
            if external_response and external_response.rr:
                print(f"✅ Recursive response from external DNS")
                # Forward the external response with correct ID
                external_response.header.id = request.header.id
                sock.sendto(external_response.pack(), addr)
            else:
                print("❌ No response from external DNS")
                reply = request.reply()
                reply.rcode = 3  # NXDOMAIN
                sock.sendto(reply.pack(), addr)
            
        except Exception as e:
            print(f"Error handling request: {e}")

if __name__ == "__main__":
    run_final_recursive_server()

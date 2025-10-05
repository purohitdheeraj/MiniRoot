import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, NS

# TLD server zone data - simulates TLD servers like .com, .org
TLD_ZONES = {
    "google.com.": {
        "NS": ["ns1.google.com.", "ns2.google.com.", "ns3.google.com.", "ns4.google.com."],
        "A": ["8.8.8.8", "8.8.4.4", "142.250.192.110", "142.250.192.111"]
    },
    "github.com.": {
        "NS": ["ns1.p16.dynect.net.", "ns2.p16.dynect.net.", "ns3.p16.dynect.net.", "ns4.p16.dynect.net."],
        "A": ["20.207.73.82", "20.207.73.83", "20.207.73.84"]
    },
    "stackoverflow.com.": {
        "NS": ["ns-1029.awsdns-00.org.", "ns-2010.awsdns-59.co.uk.", "ns-358.awsdns-44.com.", "ns-755.awsdns-30.net."],
        "A": ["104.18.32.7", "172.64.155.249", "104.18.33.7"]
    },
    "example.com.": {
        "NS": ["ns1.example.com.", "ns2.example.com."],
        "A": ["93.184.216.34", "93.184.216.35"]
    },
    "example.org.": {
        "NS": ["ns1.example.org.", "ns2.example.org."],
        "A": ["93.184.216.34", "93.184.216.35"]
    }
}

def resolve_tld_query(domain, qtype):
    """Resolve queries at the TLD server level"""
    print(f"🏢 TLD server query: {domain} ({qtype})")
    
    # Check if we have delegation for this domain
    if domain in TLD_ZONES:
        zone = TLD_ZONES[domain]
        
        if qtype == "NS":
            # Return NS records for domain delegation
            reply = DNSRecord.question(domain, "NS").reply()
            for ns in zone["NS"]:
                reply.add_answer(RR(domain, QTYPE.NS, rdata=NS(ns), ttl=3600))
            return reply
        
        elif qtype == "A":
            # Return A records for domain
            reply = DNSRecord.question(domain, "A").reply()
            for ip in zone["A"]:
                reply.add_answer(RR(domain, QTYPE.A, rdata=A(ip), ttl=3600))
            return reply
    
    return None

def run_tld_server():
    """Run the TLD DNS server simulator"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8056))  # Port 8056 for TLD server
    print("🏢 TLD DNS Server Simulator running on 127.0.0.1:8056...")
    print("📍 Simulates TLD servers (.com, .org, .net)")
    print("🔗 Knows about specific domains and their authoritative servers")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            
            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]
            
            print(f"\n📨 TLD Query: {qname} ({qtype}) from {addr}")
            
            # Try to resolve the query
            response = resolve_tld_query(qname, qtype)
            
            if response:
                print(f"✅ TLD server response for {qname}")
                sock.sendto(response.pack(), addr)
            else:
                print(f"❌ No delegation found for {qname}")
                reply = request.reply()
                reply.rcode = 3  # NXDOMAIN
                sock.sendto(reply.pack(), addr)
            
        except Exception as e:
            print(f"Error handling TLD query: {e}")

if __name__ == "__main__":
    run_tld_server()

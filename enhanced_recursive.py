import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import socket
from dnslib import DNSRecord, QTYPE, RR, A, CNAME, NS
from zone.zone_loader import load_zones

# Load our authoritative zones
zones = load_zones()

def query_dns_server(server_ip, port, query, timeout=5):
    """Query a specific DNS server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        
        # Send query
        sock.sendto(query.pack(), (server_ip, port))
        
        # Receive response
        data, addr = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        
        sock.close()
        return response
    except Exception as e:
        print(f"Error querying {server_ip}:{port}: {e}")
        return None

def resolve_authoritative(domain, qtype):
    """Resolve from our authoritative zones"""
    if domain not in zones:
        return None
    
    zone = zones[domain]
    
    # Handle A records
    if qtype == "A" and "A" in zone:
        ip = zone["A"]
        ttl = zone.get("TTL", 300)
        reply = DNSRecord.question(domain, "A").reply()
        reply.add_answer(RR(domain, QTYPE.A, rdata=A(ip), ttl=ttl))
        return reply
    
    return None

def enhanced_recursive_resolve(domain, qtype):
    """Enhanced recursive resolution using our simulated DNS hierarchy"""
    print(f"🔍 Enhanced recursive resolve: {domain} ({qtype})")
    
    # Step 1: Check if we have authoritative data
    auth_response = resolve_authoritative(domain, qtype)
    if auth_response:
        print("✅ Authoritative response")
        return auth_response
    
    # Step 2: Query root servers for TLD delegation
    print("📍 Step 1: Querying root servers for TLD delegation...")
    tld = domain.split('.')[-1] + "."
    root_query = DNSRecord.question(tld, "NS")
    
    root_response = query_dns_server("127.0.0.1", 8055, root_query)
    if not root_response or not root_response.rr:
        print("❌ No response from root servers")
        return None
    
    print(f"✅ Got TLD delegation from root servers")
    
    # Step 3: Query TLD servers for domain delegation
    print("📍 Step 2: Querying TLD servers for domain delegation...")
    tld_query = DNSRecord.question(domain, "NS")
    
    tld_response = query_dns_server("127.0.0.1", 8056, tld_query)
    if not tld_response or not tld_response.rr:
        print("❌ No response from TLD servers")
        return None
    
    print(f"✅ Got domain delegation from TLD servers")
    
    # Step 4: Query authoritative servers for final answer
    print("📍 Step 3: Querying authoritative servers for final answer...")
    
    # Extract authoritative server from TLD response
    auth_servers = []
    for rr in tld_response.rr:
        if rr.rtype == QTYPE.NS:
            auth_server = str(rr.rdata)
            auth_servers.append(auth_server)
            print(f"  🔍 Found authoritative server: {auth_server}")
    
    if not auth_servers:
        print("❌ No authoritative servers found")
        return None
    
    # Query the first authoritative server
    auth_server = auth_servers[0]
    print(f"  🔍 Querying authoritative server: {auth_server}")
    
    # Get A record for authoritative server first
    auth_a_query = DNSRecord.question(auth_server, "A")
    auth_a_response = query_dns_server("127.0.0.1", 8056, auth_a_query)
    
    if auth_a_response and auth_a_response.rr:
        for rr in auth_a_response.rr:
            if rr.rtype == QTYPE.A:
                auth_ip = str(rr.rdata)
                print(f"  ✅ Authoritative server {auth_server} -> {auth_ip}")
                
                # Now query the authoritative server for the domain
                final_query = DNSRecord.question(domain, qtype)
                final_response = query_dns_server(auth_ip, 53, final_query)
                
                if final_response:
                    print(f"✅ Got final answer from authoritative server")
                    return final_response
    
    print("❌ Could not get final answer")
    return None

def run_enhanced_recursive_server():
    """Run the enhanced recursive DNS server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8057))  # Port 8057 for enhanced recursive
    print("🚀 Enhanced Recursive DNS Server running on 127.0.0.1:8057...")
    print("🌍 Uses simulated root and TLD servers")
    print("🔗 Complete DNS hierarchy simulation")
    
    while True:
        try:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            
            qname = str(request.q.qname)
            qtype = QTYPE[request.q.qtype]
            
            print(f"\n📨 Enhanced Query: {qname} ({qtype}) from {addr}")
            
            # Try enhanced recursive resolution
            response = enhanced_recursive_resolve(qname, qtype)
            
            if response:
                print(f"✅ Enhanced recursive response")
                # Forward the response with correct ID
                response.header.id = request.header.id
                sock.sendto(response.pack(), addr)
            else:
                print("❌ No response found")
                reply = request.reply()
                reply.rcode = 3  # NXDOMAIN
                sock.sendto(reply.pack(), addr)
            
        except Exception as e:
            print(f"Error handling enhanced query: {e}")

if __name__ == "__main__":
    run_enhanced_recursive_server()

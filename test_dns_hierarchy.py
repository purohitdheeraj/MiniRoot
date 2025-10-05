#!/usr/bin/env python3
"""
Test script to demonstrate the complete DNS hierarchy
"""

import socket
from dnslib import DNSRecord, QTYPE

def test_dns_hierarchy():
    """Test the complete DNS hierarchy"""
    print("🧪 Testing Complete DNS Hierarchy")
    print("=" * 50)
    
    # Test 1: Root Server
    print("\n📍 Test 1: Root Server (Port 8055)")
    print("Querying root server for .com TLD delegation...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        query = DNSRecord.question("com.", "NS")
        sock.sendto(query.pack(), ("127.0.0.1", 8055))
        
        data, addr = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        
        print(f"✅ Root server response:")
        print(f"   Query: {query.q.qname} ({QTYPE[query.q.qtype]})")
        print(f"   Answers: {len(response.rr)} records")
        
        for rr in response.rr:
            print(f"   - {rr.rname} {QTYPE[rr.rtype]} {rr.rdata}")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Root server test failed: {e}")
    
    # Test 2: TLD Server
    print("\n📍 Test 2: TLD Server (Port 8056)")
    print("Querying TLD server for google.com delegation...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        
        query = DNSRecord.question("google.com.", "NS")
        sock.sendto(query.pack(), ("127.0.0.1", 8056))
        
        data, addr = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        
        print(f"✅ TLD server response:")
        print(f"   Query: {query.q.qname} ({QTYPE[query.q.qtype]})")
        print(f"   Answers: {len(response.rr)} records")
        
        for rr in response.rr:
            print(f"   - {rr.rname} {QTYPE[rr.rtype]} {rr.rdata}")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ TLD server test failed: {e}")
    
    # Test 3: Enhanced Recursive Resolver
    print("\n📍 Test 3: Enhanced Recursive Resolver (Port 8057)")
    print("Querying enhanced resolver for google.com...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        
        query = DNSRecord.question("google.com.", "A")
        sock.sendto(query.pack(), ("127.0.0.1", 8057))
        
        data, addr = sock.recvfrom(512)
        response = DNSRecord.parse(data)
        
        print(f"✅ Enhanced resolver response:")
        print(f"   Query: {query.q.qname} ({QTYPE[query.q.qtype]})")
        print(f"   Answers: {len(response.rr)} records")
        
        for rr in response.rr:
            print(f"   - {rr.rname} {QTYPE[rr.rtype]} {rr.rdata}")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Enhanced resolver test failed: {e}")
    
    print("\n🎉 DNS Hierarchy Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_dns_hierarchy()

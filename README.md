# Mini DNS Server

A simple DNS server implementation for learning DNS internals.

## Current Setup

### What's Implemented

- ✅ **Authoritative DNS Server** - Serves local domains from zone files
- ✅ **Recursive DNS Resolver** - Queries external DNS servers for unknown domains
- ✅ **Complete DNS Record Support** - All 8 record types (A, CNAME, NS, SOA, TXT, MX, PTR, SRV)
- ✅ **Hybrid DNS Server** - Both authoritative and recursive in one server
- ✅ **Root Server Simulator** - Simulates the 13 DNS root servers
- ✅ **TLD Server Simulator** - Simulates Top Level Domain servers (.com, .org, .net)
- ✅ **Enhanced Recursive Resolver** - Full DNS hierarchy simulation
- ✅ **Complete DNS Hierarchy** - Root → TLD → Authoritative flow
- ✅ **Zone file loading** (JSON format)
- ✅ **UDP servers** on multiple ports (8053-8057)
- ✅ **Multiple record types per domain**
- ✅ **TTL support for all records**

### Project Structure

```
mini-dns/
├── server/
│   └── dns_server.py          # Authoritative DNS server (port 8053)
├── recursive.py               # Recursive DNS resolver (port 8054)
├── root_server.py             # Root DNS server simulator (port 8055)
├── tld_server.py              # TLD DNS server simulator (port 8056)
├── enhanced_recursive.py      # Enhanced recursive resolver (port 8057)
├── test_dns_hierarchy.py      # DNS hierarchy testing script
├── simple_hierarchy_demo.py   # DNS hierarchy demonstration
├── zone/
│   ├── zones.json             # Zone configuration
│   └── zone_loader.py         # Zone file loader
└── README.md
```

## Quick Start

1. **Install dependencies**

   ```bash
   pip install dnslib
   ```

2. **Run the servers**

   ```bash
   # Individual servers
   python3 server/dns_server.py     # Authoritative DNS server (port 8053)
   python3 recursive.py             # Recursive DNS resolver (port 8054)
   
   # DNS hierarchy simulation servers
   python3 root_server.py           # Root DNS server (port 8055)
   python3 tld_server.py            # TLD DNS server (port 8056)
   python3 enhanced_recursive.py    # Enhanced recursive resolver (port 8057)
   ```

   Alternatively, you can use vscode tasks to run the servers.

   Steps:  
   1. Open the repository in vscode.
   2. Click `Ctrl+Shift+P` to open the command palette.
   3. Type `Tasks: Run Task` and press `Enter`.
   4. Select the task you want to run and press `Enter`. (Use task `Run All Servers` to run all servers at once)
   5. The server(s) will start running in the terminal.
   6. Take all the terminals to a single window and arrange them however you like. (Optional)
   
   Note: The tasks are configured in the `.vscode/tasks.json` file.

3. **Test with dig**

   ```bash
   # Authoritative Server (Port 8053) - Local domains only
   dig @127.0.0.1 -p 8053 myapp.local A
   dig @127.0.0.1 -p 8053 myapp.local NS
   dig @127.0.0.1 -p 8053 myapp.local MX
   dig @127.0.0.1 -p 8053 myapp.local SRV

   # Recursive Resolver (Port 8054) - Local + External domains
   dig @127.0.0.1 -p 8054 myapp.local A          # Local domain
   dig @127.0.0.1 -p 8054 google.com A           # External domain
   
   # Enhanced Recursive Resolver (Port 8057) - Full hierarchy simulation
   dig @127.0.0.1 -p 8057 google.com A           # Simulated hierarchy resolution
   dig @127.0.0.1 -p 8057 github.com A           # Uses root → TLD → auth flow
   ```

4. **Test DNS hierarchy simulation**

   ```bash
   # Test the complete hierarchy
   python3 test_dns_hierarchy.py
   
   # See hierarchy demonstration
   python3 simple_hierarchy_demo.py
   ```

## Current Zone Configuration

The server is configured with these records:

### Domain: myapp.local.

- **A Record**: `192.168.1.100` (IP address)
- **NS Records**: `ns1.myapp.local.`, `ns2.myapp.local.` (name servers)
- **SOA Record**: Zone authority info (serial, refresh, retry, expire, minimum)
- **MX Records**: Mail servers with priorities
  - Priority 10: `mail.myapp.local.`
  - Priority 20: `mail2.myapp.local.`
- **TXT Records**: SPF and verification strings
  - `v=spf1 include:_spf.google.com ~all`
  - `google-site-verification=abc123`

### Other Domains:

- `www.myapp.local.` → `myapp.local.` (CNAME)
- `mail.myapp.local.` → `192.168.1.101` (A record)
- `mail2.myapp.local.` → `192.168.1.102` (A record)
- `ns1.myapp.local.` → `192.168.1.103` (A record)
- `ns2.myapp.local.` → `192.168.1.104` (A record)

### Reverse DNS:

- `100.1.168.192.in-addr.arpa.` → `myapp.local.` (PTR record)

## Supported DNS Record Types

| Record Type | Purpose                | Example                                                  |
| ----------- | ---------------------- | -------------------------------------------------------- |
| **A**       | IPv4 address           | `myapp.local. A 192.168.1.100`                           |
| **CNAME**   | Canonical name (alias) | `www.myapp.local. CNAME myapp.local.`                    |
| **NS**      | Name server            | `myapp.local. NS ns1.myapp.local.`                       |
| **SOA**     | Start of authority     | Zone metadata (serial, refresh, etc.)                    |
| **MX**      | Mail exchange          | `myapp.local. MX 10 mail.myapp.local.`                   |
| **TXT**     | Text record            | `myapp.local. TXT "v=spf1 include:_spf.google.com ~all"` |
| **PTR**     | Pointer (reverse DNS)  | `100.1.168.192.in-addr.arpa. PTR myapp.local.`           |

## DNS Server Types

### **Authoritative Server** (Port 8053)

- Serves only local domains from zone files
- Fast response for known domains
- No external queries

### **Recursive Resolver** (Port 8054)

- Serves local domains (authoritative)
- Queries external DNS servers for unknown domains
- Hybrid functionality - best of both worlds

### **Root Server Simulator** (Port 8055)

- Simulates the 13 DNS root servers
- Knows about TLD servers (.com, .org, .net, .edu, .gov)
- Returns delegation information for TLD queries

### **TLD Server Simulator** (Port 8056)

- Simulates Top Level Domain servers (.com, .org, .net)
- Knows about specific domains and their authoritative servers
- Returns delegation information for domain queries

### **Enhanced Recursive Resolver** (Port 8057)

- Complete DNS hierarchy simulation
- Queries Root → TLD → Authoritative in sequence
- Demonstrates full DNS resolution process

## DNS Hierarchy Flow

### Complete DNS Resolution Simulation:

```
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐    ┌──────────────┐
│    Client   │───▶│   Enhanced      │───▶│   Root       │───▶│    TLD       │
│   (dig)     │    │   Recursive    │    │  Server     │    │  Server     │
│             │    │  (Port 8057)  │    │ (Port 8055) │    │ (Port 8056) │
└─────────────┘    └─────────────────┘    └──────────────┘    └──────────────┘
                            │                      │                   │
                            ▼                      ▼                   ▼
                    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                    │ Authoritative │    │ TLD Delegation │   │ Domain        │
                    │    Server     │    │ (.com, .org)   │   │ Delegation    │
                    │ (Port 8053)   │    │               │   │ (google.com)  │
                    └──────────────┘    └──────────────┘   └──────────────┘
```

**Resolution Steps:**
1. Client queries Enhanced Recursive (8057) for google.com
2. Enhanced Recursive queries Root Server (8055) for .com delegation
3. Root Server responds with TLD server information
4. Enhanced Recursive queries TLD Server (8056) for google.com delegation
5. TLD Server responds with authoritative server information
6. Enhanced Recursive queries authoritative servers for final answer
7. Client receives the IP address

## Learning Journey Progress

Following the DNS learning roadmap, this project has implemented:

### ✅ Completed Features
- [x] Add more record types (NS, SOA, TXT, MX, PTR, SRV)
- [x] Implement recursive resolution
- [x] Build root server simulator
- [x] Build TLD server simulator
- [x] Complete DNS hierarchy simulation
- [x] Enhanced recursive resolver with full hierarchy traversal
- [x] Testing framework for hierarchy validation

### 🚧 Next Steps
- [ ] Add caching system for performance optimization
- [ ] Implement DNSSEC (DNS Security Extensions)
- [ ] Add more realistic root server data
- [ ] Build DNS load balancing mechanisms
- [ ] Add comprehensive logging and monitoring
- [ ] Implement DNS over HTTPS (DoH)
- [ ] Add performance benchmarking tools

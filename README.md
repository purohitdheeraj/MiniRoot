# Mini DNS Server

A simple DNS server implementation for learning DNS internals.

## Current Setup

### What's Implemented

- ✅ **Authoritative DNS Server** - Serves local domains from zone files
- ✅ **Recursive DNS Resolver** - Queries external DNS servers for unknown domains
- ✅ **Complete DNS Record Support** - All 8 record types (A, CNAME, NS, SOA, TXT, MX, PTR, SRV)
- ✅ **Hybrid DNS Server** - Both authoritative and recursive in one server
- ✅ **Zone file loading** (JSON format)
- ✅ **UDP servers** on ports 8053 (authoritative) and 8054 (recursive)
- ✅ **Multiple record types per domain**
- ✅ **TTL support for all records**

### Project Structure

```
mini-dns/
├── server/
│   └── dns_server.py      # Authoritative DNS server (port 8053)
├── final_recursive.py     # Recursive DNS resolver (port 8054)
├── zone/
│   ├── zones.json         # Zone configuration
│   └── zone_loader.py     # Zone file loader
├── notes/
│   ├── DNS_RECORD_TYPES.md    # Complete record types guide
│   ├── DNS_LEARNING_ROADMAP.md # Learning progression
│   └── DNS_CONFIGURATIONS.md  # DNS architecture guide
└── README.md
```

## Quick Start

1. **Install dependencies**

   ```bash
   pip install dnslib
   ```

2. **Run the servers**

   ```bash
   # Authoritative DNS server (local domains only)
   python3 server/dns_server.py

   # Recursive DNS resolver (local + external domains)
   python3 final_recursive.py
   ```

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
   dig @127.0.0.1 -p 8054 github.com A           # External domain
   dig @127.0.0.1 -p 8054 stackoverflow.com A   # External domain
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

## Next Steps

- [x] Add more record types (NS, SOA, TXT, MX, PTR, SRV)
- [x] Implement recursive resolution
- [ ] Add caching system
- [ ] Build root server simulator
- [ ] Build TLD server simulator
- [ ] Add logging and monitoring

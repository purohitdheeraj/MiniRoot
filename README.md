# Mini DNS Server

A simple DNS server implementation for learning DNS internals.

## Current Setup

### What's Implemented

- ✅ Basic authoritative DNS server
- ✅ Complete DNS record support (A, CNAME, NS, SOA, TXT, MX, PTR)
- ✅ Zone file loading (JSON format)
- ✅ UDP server on port 8053
- ✅ Multiple record types per domain
- ✅ TTL support for all records

### Project Structure

```
mini-dns/
├── server/
│   └── dns_server.py      # Main DNS server
├── zone/
│   ├── zones.json         # Zone configuration
│   └── zone_loader.py     # Zone file loader
└── README.md
```

## Quick Start

1. **Install dependencies**

   ```bash
   pip install dnslib
   ```

2. **Run the server**

   ```bash
   python server/dns_server.py
   ```

3. **Test with dig**

   ```bash
   # A Records
   dig @127.0.0.1 -p 8053 myapp.local A

   # CNAME Records
   dig @127.0.0.1 -p 8053 www.myapp.local CNAME

   # NS Records
   dig @127.0.0.1 -p 8053 myapp.local NS

   # SOA Records
   dig @127.0.0.1 -p 8053 myapp.local SOA

   # MX Records
   dig @127.0.0.1 -p 8053 myapp.local MX

   # TXT Records
   dig @127.0.0.1 -p 8053 myapp.local TXT

   # PTR Records (Reverse DNS)
   dig @127.0.0.1 -p 8053 100.1.168.192.in-addr.arpa PTR
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

## Next Steps

- [x] Add more record types (NS, SOA, TXT, MX, PTR)
- [ ] Implement recursive resolution
- [ ] Add caching system
- [ ] Build secondary server support
- [ ] Add logging and monitoring

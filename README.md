# Mini DNS Server

A simple DNS server implementation for learning DNS internals.

## Current Setup

### What's Implemented

- ✅ Basic authoritative DNS server
- ✅ A and CNAME record support
- ✅ Zone file loading (JSON format)
- ✅ UDP server on port 8053

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
   dig @127.0.0.1 -p 8053 myapp.local
   dig @127.0.0.1 -p 8053 www.myapp.local
   ```

## Current Zone Configuration

The server is configured with these records:

- `myapp.local.` → `192.168.1.100` (A record)
- `www.myapp.local.` → `myapp.local.` (CNAME record)

## Next Steps

- [ ] Add more record types (NS, SOA, TXT)
- [ ] Implement recursive resolution
- [ ] Add caching system
- [ ] Build secondary server support


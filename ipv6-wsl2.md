# Enabling IPv6 Connectivity in WSL2 for Supabase Using Cloudflare WARP

This document provides a complete, step-by-step guide to enable full IPv6 support inside WSL2 using **Cloudflare WARP**, allowing successful connections to **Supabase PostgreSQL**, which requires IPv6-only connectivity.

---

## 1. Background

Supabase databases accept **IPv6-only** connections. By default, **WSL2 does not expose global IPv6 connectivity**, even if Windows supports it. This results in errors when connecting to Supabase from WSL2.

To solve this, we enable IPv6 for Windows using Cloudflare WARP and configure WSL2 to inherit Windows networking through `networkingMode=mirrored`.

---

## 2. Requirements

* Windows 11
* WSL2
* Cloudflare WARP installed on Windows
* Supabase project with IPv6-enabled PostgreSQL

---

## 3. Install and Activate Cloudflare WARP

1. Download Cloudflare WARP from:

   * [https://1.1.1.1/](https://1.1.1.1/)

2. Install the application.

3. Set the mode to **WARP** (not "1.1.1.1" only).

4. Click **Connect** until the status shows:

```
Connected – WARP
```

This gives Windows global IPv6 outbound access.

---

## 4. Verify IPv6 Works on Windows

Open PowerShell and run:

```powershell
ping -6 google.com
```

Expected output:

* IPv6 address
* Replies with low latency

If Windows cannot reach IPv6 hosts, WSL will not work either.

---

## 5. Configure WSL2 to Inherit Windows IPv6

Edit the file:

```powershell
notepad $env:USERPROFILE\.wslconfig
```

Add the following configuration:

```
[wsl2]
networkingMode=mirrored
ipv6=true
dnsTunneling=true
autoProxy=true
```

Explanation:

* `networkingMode=mirrored` allows WSL to use the same network stack as Windows.
* `ipv6=true` explicitly enables IPv6.
* `dnsTunneling=true` ensures DNS queries behave correctly under WARP.
* `autoProxy=true` helps with WARP routing.

---

## 6. Fully Restart WSL

Run:

```powershell
wsl --shutdown
```

Ensure in Task Manager that no `vmmem`, `vmmemWSL`, or `wslhost.exe` processes remain.

Then re-open WSL.

---

## 7. Validate IPv6 Inside WSL

Inside WSL, run:

```bash
ip -6 addr
```

Expected:

* Link-local IPv6 address (`fe80::...`)
* **Global IPv6 address** (`2606:4700:...` or `2xxx:...`)

Then test IPv6 connectivity:

```bash
ping -6 google.com
```

Expected: successful replies.

---

## 8. Test IPv6 Access to Supabase

### Check resolution:

```bash
ping -6 db.<your-supabase>.supabase.co
```

Supabase may ignore ICMPv6 (ping), so failure here is normal.

### Instead, test TCP connectivity:

```bash
nc -vz db.<your-supabase>.supabase.co 5432
```

Expected:

```
Connection succeeded!
```

This confirms that WSL → IPv6 → Supabase is working.

---

## 9. Full Supabase Database Connectivity Test

Save the following file as `test_supabase_connection.py`:

```python
import os
import socket
import psycopg2

def resolve_ipv6(hostname: str):
    print(f"Resolving IPv6 for: {hostname}")
    result = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    ipv6_list = [r[4][0] for r in result]
    print(f"IPv6 addresses: {ipv6_list}")
    return ipv6_list


def check_port(hostname: str, port: int):
    print(f"Checking TCP connectivity to {hostname}:{port}")
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((hostname, port))
        print("TCP connection succeeded!")
    finally:
        sock.close()


def test_postgres_connection():
    host = os.getenv("SUPABASE_DB_HOST")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")
    database = os.getenv("SUPABASE_DB_NAME", "postgres")

    print("Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=database,
        sslmode="require",
    )

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    print(f"Query result: {result}")

    cur.close()
    conn.close()
    print("PostgreSQL connection OK!")


if __name__ == "__main__":
    host = os.getenv("SUPABASE_DB_HOST")

    if not host:
        raise RuntimeError("Environment variable SUPABASE_DB_HOST is not set.")

    resolve_ipv6(host)
    check_port(host, 5432)
    test_postgres_connection()
```

### Install dependencies:

```bash
pip install psycopg2-binary
```

### Run the test:

```bash
python test_supabase_connection.py
```

Expected:

* IPv6 resolutions
* TCP success
* `Query result: (1,)`

This confirms full Supabase IPv6 connectivity.

---

## 10. Summary

| Step                    | Description                        |
| ----------------------- | ---------------------------------- |
| Install Cloudflare WARP | Enables IPv6 on Windows            |
| Configure `.wslconfig`  | Enables IPv6 + mirrored networking |
| Restart WSL             | Applies new network mode           |
| Validate IPv6           | Ensure WSL has a global IPv6       |
| Test Supabase           | Confirm IPv6 TCP connectivity      |
| Run Python test         | Ensure PostgreSQL connection works |

---

Your WSL environment now has full IPv6 connectivity through Cloudflare WARP and can connect to Supabase without issues.

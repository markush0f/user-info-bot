import os
import psycopg2
import socket
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(Path.cwd() / ".env")


def resolve_ipv6(hostname: str):
    """Resolve an AAAA record."""
    print(f"Resolving IPv6 for: {hostname}")
    result = socket.getaddrinfo(hostname, None, socket.AF_INET6)
    ipv6_list = [r[4][0] for r in result]
    print(f"IPv6 addresses: {ipv6_list}")
    return ipv6_list


def check_port(hostname: str, port: int):
    """Check if the remote IPv6 port is reachable."""
    print(f"Checking TCP connectivity to {hostname}:{port}")
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((hostname, port))
        print("TCP connection succeeded!")
    finally:
        sock.close()


def test_postgres_connection():
    """Connect to Supabase and run a simple test query."""
    host = os.getenv("HOST")
    user = os.getenv("USER_DB")
    password = os.getenv("PASSWORD_DB")
    database = os.getenv("DATABASE", "postgres")

    print("Connecting to Supabase PostgreSQL...")
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=database,
    )

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    print(f"Query result: {result}")

    cur.close()
    conn.close()
    print("PostgreSQL connection OK!")


if __name__ == "__main__":
    host = os.getenv("HOST")

    if not host:
        raise RuntimeError("Environment variable HOST is not set.")

    resolve_ipv6(host)
    check_port(host, 5432)
    test_postgres_connection()

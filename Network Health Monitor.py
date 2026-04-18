import socket
import time
import csv
from datetime import datetime

# --- Configuration ---
# List of DNS servers to benchmark
DNS_SERVERS = [
    {"name": "AdGuard", "ip": "94.140.14.14"},
    {"name": "AliDNS", "ip": "223.5.5.5"},
    {"name": "OpenDNS", "ip": "208.67.222.222"},
    {"name": "CleanBrowsing", "ip": "185.228.168.9"},
    {"name": "Cloudflare", "ip": "1.1.1.1"},
    {"name": "ControlD", "ip": "76.76.2.0"},
    {"name": "DNS.SB", "ip": "185.222.222.222"},
    {"name": "DNSPod", "ip": "119.29.29.29"},
    {"name": "Google", "ip": "8.8.8.8"},
    {"name": "Mullvad", "ip": "194.242.2.2"},
    {"name": "Mullvad Base", "ip": "194.242.2.4"},
    {"name": "NextDNS", "ip": "45.90.28.0"},
    {"name": "OpenBLD", "ip": "146.112.41.2"},
    {"name": "DNS4EU", "ip": "86.54.11.100"},
    {"name": "Quad9", "ip": "9.9.9.9"},
    {"name": "360", "ip": "101.226.4.6"},
    {"name": "Canadian Shield", "ip": "149.112.121.10"},
    {"name": "Digitale Gesellschaft", "ip": "185.95.218.42"},
    {"name": "DNS for Family", "ip": "94.130.180.225"},
    {"name": "Restena", "ip": "158.64.1.29"},
    {"name": "IIJ", "ip": "203.180.164.45"},
    {"name": "LibreDNS", "ip": "116.202.176.26"},
    {"name": "Switch", "ip": "130.59.31.248"},
    {"name": "Foundation for Applied Privacy", "ip": "146.255.56.98"},
    {"name": "UncensoredDNS", "ip": "91.239.100.100"},
    {"name": "RethinkDNS", "ip": "104.21.83.62"},
    {"name": "FlashStart", "ip": "185.236.104.104"},
    {"name": "Comcast Xfinity", "ip": "75.75.75.75"}
]
TEST_PORT = 53  # DNS port
TIMEOUT = 1.5   # Reduced timeout for faster bulk checking

def check_connection(host, port=TEST_PORT, timeout=TIMEOUT):
    """
    Attempts to establish a TCP connection to the target server.
    Returns a tuple: (is_connected (bool), latency_in_ms (float or None))
    """
    try:
        # Create a socket (IPv4, TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Measure the time it takes to connect
        start_time = time.time()
        sock.connect((host, port))
        end_time = time.time()
        
        sock.close()
        
        latency = round((end_time - start_time) * 1000, 2) # Convert to milliseconds
        return True, latency
    except (socket.timeout, socket.error):
        # Connection failed (Network down or high packet loss)
        return False, None

def main():
    print("Starting One-Time DNS Server Benchmark...\n")
    print(f"{'DNS Provider':<35} | {'IP Address':<15} | {'Status':<6} | {'Latency (ms)':<12}")
    print("-" * 75)
    
    results = []

    for server in DNS_SERVERS:
        is_connected, latency = check_connection(host=server['ip'])
        status = "UP" if is_connected else "DOWN"
        latency_str = f"{latency} ms" if latency is not None else "N/A"
        
        print(f"{server['name']:<35} | {server['ip']:<15} | {status:<6} | {latency_str:<12}")
        
        if is_connected:
            results.append((server['name'], server['ip'], latency))
    
    if results:
        results.sort(key=lambda x: x[2])  # Sort by latency
        fastest = results[0]
        print("\n" + "=" * 75)
        print(f"🏆 Fastest DNS Server: {fastest[0]} ({fastest[1]}) with {fastest[2]} ms")
        print("=" * 75)

if __name__ == "__main__":
    main()

import socket
import time
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Configuration ---
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

TEST_PORT = 53
TIMEOUT = 1.5
MAX_WORKERS = 20


# --- Core Function ---
def check_connection(server):
    ip = server["ip"]
    name = server["name"]

    try:
        start = time.perf_counter()

        with socket.create_connection((ip, TEST_PORT), timeout=TIMEOUT):
            latency = (time.perf_counter() - start) * 1000

        return {
            "name": name,
            "ip": ip,
            "status": "UP",
            "latency": round(latency, 2)
        }

    except Exception:
        return {
            "name": name,
            "ip": ip,
            "status": "DOWN",
            "latency": None
        }


# --- Benchmark Runner ---
def run_benchmark():
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_connection, server) for server in DNS_SERVERS]

        for future in as_completed(futures):
            results.append(future.result())

    return results


# --- Display Results ---
def display_results(results):
    print("\nStarting DNS Benchmark...\n")
    print(f"{'DNS Provider':<35} | {'IP Address':<15} | {'Status':<6} | {'Latency (ms)':<12}")
    print("-" * 75)

    for r in results:
        latency = f"{r['latency']} ms" if r['latency'] else "N/A"
        print(f"{r['name']:<35} | {r['ip']:<15} | {r['status']:<6} | {latency:<12}")

    valid = [r for r in results if r["status"] == "UP"]

    if valid:
        valid.sort(key=lambda x: x["latency"])
        fastest = valid[0]

        print("\n" + "=" * 75)
        print(f"🏆 Fastest DNS: {fastest['name']} ({fastest['ip']}) → {fastest['latency']} ms")
        print("=" * 75)


# --- Export CSV ---
def export_csv(results):
    filename = f"dns_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Provider", "IP", "Status", "Latency(ms)"])

        for r in results:
            writer.writerow([r["name"], r["ip"], r["status"], r["latency"]])

    print(f"\n📁 Results saved to {filename}")


# --- Main ---
def main():
    start_time = time.time()

    results = run_benchmark()
    results.sort(key=lambda x: x["latency"] if x["latency"] else 999)

    display_results(results)

    export_csv(results)

    print(f"\n⏱️ Completed in {round(time.time() - start_time, 2)} seconds")


if __name__ == "__main__":
    main()

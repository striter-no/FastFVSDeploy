#!/usr/bin/env python3
import socket
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor

OUTPUT = ""
printing = True
progress = 0
bar = 20

def ping_scan(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
    except socket.error as e:
        if e.errno == socket.errno.ECONNREFUSED:
            return 0  # Connection refused (RST packet received)
        elif e.errno == socket.errno.TIMEDOUT:
            return -1  # No response or other error (filtered or unreachable)
        else:
            print(f"Error connecting to {ip}:{port}: {e}")
            return 0
    else:
        # Connection established (port is open)
        sock.close()
        return 1

def scan_port(ip, port, num, ignore_unk, ignore_closed):
    global OUTPUT
    global progress

    progress += 1
    
    if not printing: 
        proc = (progress/num)*bar
        
        ln = "-" * round(proc)
        pn = "." * (bar - round(proc))
        print(f"\rprogress: {proc/bar:.2f}% [{ln}{pn}]", end="  \r")

    res = ping_scan(ip, port)
    if printing: 
        print(f"\rscanning: {port}/{num}: {res}", end="  \r")
    if res != -1:
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "unknown"
            if ignore_unk:
                # print(f"Unknown service for port {port} (ignored)")
                return
        if res == 0 and not ignore_closed:
            OUTPUT += f"{port}: closed: may be: {service}\n"
            if printing: 
                print(f"{port}: closed: may be: {service}")
        elif res == 1:
            OUTPUT += f"{port}: open: may be: {service}\n"
            if printing: 
                print(f"{port}: open: may be: {service}")
    else:
        global filtered
        filtered += 1

def main(ip, ports, workers, ignore_unk, ignore_closed):
    global filtered
    global OUTPUT

    filtered = 0
    num_ports = len(ports)
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for port in ports:
                executor.submit(scan_port, ip, port, num_ports, ignore_unk, ignore_closed)
    except Exception as e:
        OUTPUT += f"An error occurred: {e}\n"
        print(f"An error occurred: {e}")
        return

    OUTPUT += f"Not shown: {filtered} ports (no response or unreachable)\n"
    if True: 
        print(f"Not shown: {filtered} ports (no response or unreachable)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network mu;tithread TCP socket scan')
    parser.add_argument('--target', help='Target IP address', required=True)
    parser.add_argument('--ports', nargs='+', type=int, help='Ports to scan', default=None)
    parser.add_argument('--diap', nargs=2, type=int, help='Ports range to scan', default=None)
    parser.add_argument('--workers', type=int, help='Workers to execute threads', default=200)
    parser.add_argument('--output', help='Output file path', default=None)
    parser.add_argument('--ignore-unknown', action='store_true', help='Ignore unknown ports')
    parser.add_argument('--ignore-closed', action='store_true', help='Ignore closed ports')
    args = parser.parse_args()

    printing = args.output is None

    host = args.target  # Replace with the target host
    if args.diap is not None:
        start_port, end_port = args.diap
        ports_to_scan = range(start_port, end_port + 1)
    elif args.ports is not None:
        ports_to_scan = args.ports
    else:
        ports_to_scan = [i for i in range(0, 65535)]

    try:
        main(host, ports_to_scan, args.workers, args.ignore_unknown, args.ignore_closed)
    except KeyboardInterrupt:
        OUTPUT += "Scan interrupted\n"
        print("Scan interrupted")

    if args.output is not None:
        with open(args.output, 'w') as f:
            f.write(OUTPUT)
        print(f"Scan results saved to {args.output}")
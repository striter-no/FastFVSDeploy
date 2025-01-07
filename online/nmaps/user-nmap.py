import scapy.all as scapy
import subprocess
import platform
import ipaddress

def ping(host):
    """Отправляет ping запрос на указанный хост."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

import scapy.all as scapy

def syn_scan(ip, port):
    packet = scapy.IP(dst=ip) / scapy.TCP(dport=port, flags='S')
    response = scapy.sr1(packet, timeout=1, verbose=0)
    if response:
        if response.haslayer(scapy.TCP):
            if response.getlayer(scapy.TCP).flags == 0x12:  # SYN-ACK
                return True
    return False

def main(network):
    print(f"Scanning network: {network}")
    for ip in ipaddress.IPv4Network(network):
        if ping(str(ip)):
            print(f"{str(ip)} - available")
            open_ports = []
            for port in [22, 80, 443]:  # Scan specific ports
                if syn_scan(str(ip), port):
                    open_ports.append(port)
            if open_ports:
                print(f"Open ports on {str(ip)}: {open_ports}")
            else:
                print(f"No open ports on {str(ip)}")

if __name__ == "__main__":
    target = "3.87.167.154"  # Replace with target IP
    main(ipaddress.IPv4Network(target + '/32'))
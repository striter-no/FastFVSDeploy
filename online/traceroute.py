import scapy.all as scapy
import ipaddress

def traceroute(target, max_hops=30, timeout=1):
    ttl = 1
    reached_destination = False

    while not reached_destination and ttl <= max_hops:
        packet = scapy.IP(ttl=ttl, dst=target) / scapy.ICMP()
        reply = scapy.sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            print(f"{ttl}: *")
        elif reply.type == 11:
            print(f"{ttl}: {reply.src}")
        elif reply.type == 0:
            print(f"{ttl}: {reply.src} (destination reached)")
            reached_destination = True
        else:
            print(f"{ttl}: {reply.src} (unexpected response)")

        ttl += 1

if __name__ == "__main__":
    target = "8.8.8.8"  # Replace with your target IP or domain
    traceroute(target)
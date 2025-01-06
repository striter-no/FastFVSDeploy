from scapy.all import *

def syn_scan(target_ip, ports):
    for port in ports:
        # Создание SYN-пакета
        syn_packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
        
        # Отправка пакета и получение ответа
        response = sr1(syn_packet, timeout=1, verbose=0)
        
        if response is None:
            print(f"Port {port} is filtered (no response)")
        elif response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK
                print(f"Port {port} is open")
                # Отправляем RST для закрытия соединения
                rst_packet = IP(dst=target_ip)/TCP(dport=port, flags='R')
                send(rst_packet, verbose=0)
            elif response[TCP].flags == 0x14:  # RST
                print(f"Port {port} is closed")

# Пример использования
target = "192.168.1.1"  # Замените на целевой IP
ports_to_scan = [22, 80, 443]  # Замените на порты для сканирования
syn_scan(target, ports_to_scan)

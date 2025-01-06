import asyncio
import argparse
from scapy.all import *
import socket  # Импортируем библиотеку socket

async def send_syn(target_ip, port):
    # Создание SYN-пакета
    syn_packet = IP(dst=target_ip)/TCP(dport=port, flags='S')
    ports = {}  # Список для хранения открытых портов
    
    try:
        # Отправка пакета и получение ответа
        response = sr1(syn_packet, timeout=1, verbose=0)
        
        if response is None:
            pass
            # print(f"Port {port} is filtered (no response)")
        elif response.haslayer(TCP):
            if response[TCP].flags == 0x12:  # SYN-ACK
                service_name = socket.getservbyport(port)  # Получаем имя сервиса
                ports[port] = ["open", service_name]  # Добавляем имя сервиса
                # Отправляем RST для закрытия соединения
                rst_packet = IP(dst=target_ip)/TCP(dport=port, flags='R')
                send(rst_packet, verbose=0)
            elif response[TCP].flags == 0x14:  # RST
                service_name = socket.getservbyport(port)
                ports[port] = ["closed", service_name]
                # print(f"Port {port} is closed")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    
    return ports  # Возвращаем список открытых портов

async def ascan_ip(target_ip, ports):
    tasks = []
    open_ports = {}  # Список для хранения открытых портов
    for port in ports:
        tasks.append(send_syn(target_ip, port))
    
    results = await asyncio.gather(*tasks)
    
    for result in results:
        for (key, value) in result.items():
            open_ports[key] = value
    
    return open_ports  # Возвращаем список открытых портов

def scan_ip(target_ip, ports):
    return asyncio.run(ascan_ip(target_ip, ports))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='network SYN scan')
    parser.add_argument('target', help='Target IP address')
    # parser.add_argument('--ports', nargs='+', type=int, help='Ports to scan', default=[80, 443])
    args = parser.parse_args()

    # target = "192.168.31.1"  # Замените на целевой IP
    # ports_to_scan = [22, 80, 443]  # Замените на порты для сканирования
    
    target = args.target
    ports_to_scan = [22, 80, 443]  

    print(scan_ip(target, ports_to_scan))

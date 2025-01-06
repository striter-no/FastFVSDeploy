from async_pseudo_nmap import scan_ip
from requests import get
from bs4 import BeautifulSoup
import socket
import subprocess

url = "https://www.pythonanywhere.com/whitelist/"

def is_real_address(domain: str) -> bool:
    try:
        # Пытаемся получить IP-адрес по доменному имени
        ip = socket.gethostbyname(domain)
        if ip == "0.0.0.0":
            return False
        return True  # Если удалось получить IP, значит, это реальный адрес
    except:
        return False

def full_scan(ip: str):
    op_ports = scan_ip(ip, [i for i in range(1024, 49152)])
    if len(op_ports)!= 0:
        print(f"Open ports for {ip}:\n{"\n\t".join([f"port: {port} state: {state} name: {name}" for (port, (state, name)) in op_ports.items()])}")
        input("Intersting ports found > ")

import subprocess

def nmap_scan(ip: str) -> dict:
    try:
        # Выполняем команду nmap и получаем вывод
        result = subprocess.run(['nmap', ip], capture_output=True, text=True)
        output = result.stdout
        
        ports_info = {}
        
        # Обрабатываем вывод nmap
        for line in output.splitlines():
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                port = parts[0].split('/')[0]  # Порт
                socket_type = parts[0].split('/')[1]  # Тип сокета (tcp/udp)
                state = parts[1]  # Состояние порта
                service = parts[2] if len(parts) > 2 else 'unknown'  # Сервис, если указан
                
                ports_info[port] = [socket_type, state, service]
        
        return ports_info
    except Exception as e:
        print(f"Ошибка при выполнении nmap для {ip}: {e}")
        return {}


def main(ips: list[str]):
    for i, ip in enumerate(ips):
        print(f"Current ip: {ip} checking...")
        if not ip:
            print(f"\rSkipping non-real address: {ip} ({i+1}/{len(ips)})")
            continue
        elif is_real_address(ip[1:]):
            ip = ip[1:]
        elif not is_real_address(ip):
            print(f"\rSkipping non-real address: {ip} ({i+1}/{len(ips)})")
            continue

        results = nmap_scan(ip)
        
        with open("mass-scan-log.txt", "a") as file:
            text = f"Open ports for {ip}:\n\t{"\n\t".join([f"port: {port}/{prot}   state: {state}   name: {name}" for (port, (prot, state, name)) in results.items()])}\n"
            file.write(text)
            print(text)
        
        with open("mass-proxy-scan.txt", "a") as file:
            for (port, (prot, state, name)) in results.items():
                if "proxy" in name:
                    text = f"ip:{ip}  port: {port}/{prot}   state: {state}   name: {name}\n"
                    file.write(text)
                    print(f"[!] Proxy found: {text}")

        # print()
        # ports = [22, 21, 2121, 8000, 8080, 8443, 110, 143, 3306, 5432]
        # op_ports = scan_ip(ip, ports)
        # if list(op_ports.keys()) in [443, 80]:
        #     print(f"Nothing intersting at {ip}")
        #     print(f"Open ports for {ip}:\n{"\n\t".join([f"port: {port} state: {state} name: {name}" for (port, (state, name)) in op_ports.items()])}")
        # elif len(op_ports) != 0:
        #     print(f"Open ports for {ip}:\n{"\n\t".join([f"port: {port} state: {state} name: {name}" for (port, (state, name)) in op_ports.items()])}")
        #     cmd = input("Intersting ports found > ")
        #     if cmd == "full":
        #         print("Starting deep analise")
        #         full_scan(ip)
        # else:
            # print(f"No ports found at {ip} by flat analisis. Starting deep analise")
            # op_ports = scan_ip(ip, [i for i in range(1024, 49152)])
            # if len(op_ports)!= 0:
            #     print(f"Open ports for {ip}:\n{"\n\t".join([f"port: {port} state: {state} name: {name}" for (port, (state, name)) in op_ports.items()])}")
            #     input("Intersting ports found > ")

if __name__ == "__main__":
    with open("ips.html", "w") as file:
        file.write(get(url).text)

    with open("ips.html", "r") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')

    ips = []

    with open("ips.txt", "w") as file:
        for row in rows:
            cells = row.find_all('td')
            for cell in cells:
                ips.append(cell.get_text()) 
                file.write(cell.get_text()+'\n')
    
    main(ips)
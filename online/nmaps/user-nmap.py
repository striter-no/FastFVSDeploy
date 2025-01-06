import socket
import subprocess
import platform
import ipaddress

def ping(host):
    """Отправляет ping запрос на указанный хост."""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

def scan_ports(host, ports):
    """Сканирует указанные порты на заданном хосте."""
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Устанавливаем таймаут в 1 секунду
            result = sock.connect_ex((host, port))  # Пытаемся подключиться к порту
            print(f"Result: {result}")
            if result == 0:  # Если результат равен 0, порт открыт
                open_ports.append(port)
            sock.close()  # Закрываем сокет
        except socket.error as e:
            print(f"Ошибка при подключении к {host}:{port} - {e}")
    return open_ports

def main(network):
    """Основная функция сканирования сети."""
    print(f"Сканирование сети: {network}")
    # Генерируем адреса в указанной сети
    for ip in ipaddress.IPv4Network(network):
        if ping(str(ip)):
            print(f"{str(ip)} - доступен")
            # Сканируем порты 22 (SSH), 80 (HTTP), 443 (HTTPS)
            open_ports = scan_ports(str(ip), [22, 80, 443])
            if open_ports:
                print(f"Открытые порты на {str(ip)}: {open_ports}")
            else:
                print(f"Нет открытых портов на {str(ip)}")

if __name__ == "__main__":
    target = "3.87.167.154"  # Замените на целевой IP
    ports_to_scan = [i for i in range(0, 65535)]  # Замените на порты для сканирования
    scaned_ports = scan_ports(target, ports_to_scan)
    for port in ports_to_scan:
        if port in scaned_ports:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed/filtered")
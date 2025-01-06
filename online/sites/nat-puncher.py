import socket
import stun

def detect_nat_type():
    # Укажите STUN-сервер и порт
    stun_host = "stun.l.google.com"
    stun_port = 19302

    # Создайте UDP сокет
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Установите таймаут для сокета
    s.settimeout(2)

    # Укажите локальный IP и порт
    source_ip = "0.0.0.0"  # или используйте ваш локальный IP
    source_port = 54320

    # Привяжите сокет к локальному IP и порту
    s.bind((source_ip, source_port))

    # Выполните NAT-детекцию
    nat_type, external_ip = stun.get_nat_type(s, source_ip, source_port, stun_host, stun_port)

    # Закройте сокет
    s.close()

    # Вывод результатов
    print(f"NAT Type: {nat_type}")
    print(f"External IP: {external_ip}")
    # print(f"External Port: {external_port}")

if __name__ == "__main__":
    detect_nat_type()

# /etc/systemd/system/tornado.service
# /etc/nginx/sites-available/default
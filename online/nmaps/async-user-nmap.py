import asyncio
import argparse
import socket

async def scan_port(host, port):
    conn = asyncio.open_connection(host, port)
    try:
        service_name = socket.getservbyport(port)
    except:
        service_name = "unknown"

    try:
        _, writer = await asyncio.wait_for(conn, timeout=1)
        print(f'Порт {port} открыт: {service_name}')
        writer.close()
        await writer.wait_closed()
    except (asyncio.TimeoutError, ConnectionRefusedError):
        pass
        # print(f'Порт {port} закрыт или недоступен: {service_name}')
    except Exception as e:
        print(f'Ошибка при сканировании порта {port}: {e}')

async def scan_ports(host, ports):
    tasks = []
    for port in ports:
        tasks.append(scan_port(host, port))
    await asyncio.gather(*tasks)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='network ASYNK TCP SOCKET scan')
    parser.add_argument('--target', help='Target IP address', required=True)
    parser.add_argument('--ports', nargs='+', type=int, help='Ports to scan', default=[80, 443])
    parser.add_argument('--diap', nargs='+', type=int, help='Ports diaposone to scan', default=None)
    args = parser.parse_args()

    # '3.87.167.154'
    host = args.target # Замените на нужный хост
    if args.diap is None:
        ports_to_scan = args.ports  # Сканируем порты с 1 по 1024
    else:
        ports_to_scan = range(args.diap[0], args.diap[1] + 1)  # Сканируем порты в указанном диапазоне

    asyncio.run(scan_ports(host, ports_to_scan))
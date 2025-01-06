import asyncio
import socket

async def scan_port(host, port):
    conn = asyncio.open_connection(host, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=1)
        print(f'Порт {port} открыт')
        writer.close()
        await writer.wait_closed()
    except (asyncio.TimeoutError, ConnectionRefusedError):
        print(f'Порт {port} закрыт или недоступен')
    except Exception as e:
        print(f'Ошибка при сканировании порта {port}: {e}')

async def scan_ports(host, ports):
    tasks = []
    for port in ports:
        tasks.append(scan_port(host, port))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    host = '3.87.167.154'  # Замените на нужный хост
    ports_to_scan = range(1, 1025)  # Сканируем порты с 1 по 1024

    print(asyncio.run(scan_ports(host, ports_to_scan)))
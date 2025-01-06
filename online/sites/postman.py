import requests
import json

def post_request(ip, port, payload, headers=None, raw_mode=False):
    url = f"{ip}:{port}"
    
    if raw_mode:
        headers = headers or {}
        headers_str = "\r\n".join(f"{key}: {value}" for key, value in headers.items())
        request_line = payload
        response = requests.post(url, data=request_line, headers={'Content-Type': 'text/plain'}, verify=False)
    else:
        if isinstance(payload, dict):
            payload = json.dumps(payload)
            headers = headers or {}
            headers['Content-Type'] = 'application/json'
        
        response = requests.post(url, data=payload, headers=headers)
    
    return response.status_code, response.text

if __name__ == "__main__":
    ip = input("Введите IP-адрес: ")
    port = input("Введите порт: ")
    mode_choice = input("Выберите режим (json/raw): ").strip().lower()
    
    if mode_choice == 'json':
        payload = {}
        while True:
            key = input("Введите ключ (или '\\0' для завершения): ")
            if key.lower() == '\\0':
                break
            value = input(f"Введите значение для '{key}': ")
            payload[key] = value
    else:
        payload = input("Введите полезную нагрузку: ")
    
    headers_input = input("Введите заголовки в формате 'ключ: значение' (или '\\0' для завершения): ")
    headers = {}
    while headers_input.lower() != '\\0':
        key, value = headers_input.split(':', 1)
        headers[key.strip()] = value.strip()
        headers_input = input("Введите заголовки в формате 'ключ: значение' (или '\\0' для завершения): ")
    
    raw_mode = mode_choice == 'raw'
    status_code, response_text = post_request(ip, port, payload, headers, raw_mode)
    print(f"Статус код: {status_code}")
    print(f"Ответ: {response_text}")

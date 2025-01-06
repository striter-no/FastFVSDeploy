import requests

def test_proxy(proxy):
    try:
        response = requests.get('http://myexternalip.com/json', proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code != 200:
            return (False, f"Error: {response.status_code}")
        # print(f"Прокси {proxy} работает. Ответ: {response.json()}")
    except requests.exceptions.RequestException as e:
        # print(f"Прокси {proxy} не работает. Ошибка: {e}")
        return (False, str(e))
    except ValueError:
        # print(f"Прокси {proxy} вернул некорректный ответ: {response.text}")  # Добавлено для вывода текста ответа
        return (False, f"Incorrect answer: {response.text}")
    except:
        # print(f"Прокси {proxy} не удалось протестировать. Ошибка неизвестна.")
        return (False, "")
    return (True, "Success")

def main(N, proxies: list[str]) -> None:
    result = test_proxy(proxies[N])
    if result[0]:
        print(f"[V] Прокси {proxies[N]} успешно протестирован.")
    else:
        print(f"[x] Прокси {proxies[N]} не удалось протестировать: {result[1]}")
    
if __name__ == "__main__":
    with open('mass-proxy-scan.txt', 'r') as file:
        proxies = [line.split()[0][3:] + ':' + line.split()[2][:line.split()[2].index('/')] for line in file.readlines() if 'open' in line]

    for i in range(len(proxies)):
        main(i, proxies)
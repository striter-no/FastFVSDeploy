import asyncio
import os

global_insecure = []
total_items = 0

async def check_permissions(permissions, path, proceed):
    global global_insecure
    if permissions in ['0777', '0775']:
        print(f"Неправильные права доступа: для пути: {path} (из {proceed})")
        global_insecure.append((path, permissions))
    elif permissions in ['1777', '1775']:
        print(f"Подозрительные права доступа: {permissions} для пути: {path} (из {proceed})")
        global_insecure.append((path, permissions))
        # input()
    # else:
    #     print(f"{permissions} для: {path}")

# Загрузка игнорируемых директорий из файла ignore.txt
def load_ignore_list():
    try:
        with open('ignore.txt', 'r') as f:
            return {line.strip() for line in f if line.strip()}  # Возвращаем множество игнорируемых директорий
    except FileNotFoundError:
        return set()  # Если файл не найден, возвращаем пустое множество


async def find_files_and_directories():
    global total_items
    ignore_list = load_ignore_list()
    print("Проверка прав доступа для всех файлов и директорий внутри контейнера:")
    processed_items = 0

    
    # total_dirs = sum(len(dirs) for _, dirs, _ in os.walk('/'))  # Общее количество директорий
    
    total_items = 0# total_dirs + sum(len(files) for _, _, files in os.walk('/'))  # Общее количество файлов

    for root, dirs, files in os.walk('/'):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_list]

        total_dirs = len(dirs)  # Считаем количество директорий
        total_files = len(files)  # Считаем количество файлов
        total_items += total_dirs + total_files  # Обновляем общее количество элементов

        for item in dirs + files:
            path = os.path.join(root, item)
            try:
                permissions = oct(os.stat(path).st_mode)[-4:]  # Получаем права доступа
                # input(permissions)
            except Exception as e:
                with open('./log.txt', 'a') as log_file:
                    log_file.write(f"Ошибка доступа к {path}: {str(e)}\n")
                continue
            await check_permissions(permissions, path, processed_items)
            processed_items += 1
            # total_items+=1
        
            # print(f"\rПрогресс: {processed_items/total_items*100:.2f}%", end='')  # Обновляем прогресс-бар
            # print(f"\rПрогресс: {processed_items}", end='')  # Обновляем прогресс-бар
    # print()  # Переход на новую строку после завершения

async def main():
    await find_files_and_directories()

if __name__ == "__main__":
    asyncio.run(main())

    with open("insecure.txt", "w") as f:
        sorted_insecure = sorted(global_insecure, key=lambda x: (x[1] != '1777', x[1] != '1775', x[1] != '777', x[1] != '775'))
        for (path, perm) in sorted_insecure:
            f.write(f"{perm}: {path}\n")

    print(f"\nОбнаружено неправильных прав доступа к {len(global_insecure)} ({len(global_insecure)/total_items*100:.2f}%) директориям/файлам:")
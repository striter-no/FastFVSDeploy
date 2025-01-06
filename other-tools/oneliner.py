# terminals/oneliner.py

import sys

def main():
    if len(sys.argv) != 2:
        print("Использование: python oneliner.py <путь_к_файлу>")
        return

    file_path = sys.argv[1]

    with open(file_path, 'r') as file:
        code = file.read()

    # Формируем строку с exec
    result = f'exec("""{code}""")'
    print(result)

if __name__ == "__main__":
    main()
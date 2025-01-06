exec("""import subprocess
import sys
import os
import readline  # Импортируем библиотеку readline

def terminal_emulator():
    # Вывод путей к интерпретатору Python и к файлу программы
    print(f"Python interpreter path: {sys.executable}")
    print(f"Script path: {os.path.abspath(__file__)}")

    # Список для хранения истории команд
    history = []

    while True:
        command = input(">> ")
        if command.lower() in ['exit', 'quit']:
            print("exiting...")
            break
        
        # Добавляем команду в историю
        if command:
            history.append(command)
            readline.add_history(command)

        try:
            # Изменение на использование Popen для обработки ввода
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Чтение вывода в реальном времени
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Обработка ошибок
            stderr = process.stderr.read()
            if stderr:
                print(f"Err: {stderr.strip()}")
                
        except Exception as e:
            print(f"Error: {e}")

def terminal_emulator_batch(commands):
    for command in commands:
        try:
            # Изменение на использование Popen для обработки ввода
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Чтение вывода в реальном времени
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Обработка ошибок
            stderr = process.stderr.read()
            if stderr:
                print(f"Err: {stderr.strip()}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    terminal_emulator()
    # terminal_emulator_batch([
    #     "ifconfig",
    #     "ip addr",
    #     "curl -s \"myexternalip.com/raw\""
    # ])""")
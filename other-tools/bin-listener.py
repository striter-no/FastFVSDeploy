def write_binary_file(binary_string, file_path):
    with open(file_path, 'ab') as file:
        binary_data = bytes((ord(char) - 256) for char in binary_string)
        file.write(binary_data)

# Пример использования
if __name__ == "__main__":
    file_path = '/var/lock/spoofdpi'  # Укажите путь к вашему бинарному файлу
    data = input("bin >> ")
    while data != "exit":
        write_binary_file(data, file_path)
        data = input("bin >> ")
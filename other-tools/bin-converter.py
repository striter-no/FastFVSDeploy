import pyperclip

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return ''.join(chr(256+byte) for byte in binary_data)

def split_binary_string(binary_string, bytes_per_line=64):
    lines = [binary_string[i:i+bytes_per_line] for i in range(0, len(binary_string), bytes_per_line)]
    return '\n'.join(lines)

# Пример использования
if __name__ == "__main__":
    file_path = './spoofdpi'  # Укажите путь к вашему бинарному файлу
    binary_string = read_binary_file(file_path)
    chunks = split_binary_string(binary_string, 2**20)
    list_chunks = chunks.split('\n')

    with open(f"{file_path}.converted.txt", "w") as f:
        f.write(chunks)
    print(f"Chunks: {chunks.count('\n')}")

    for i, chunk in enumerate(list_chunks):
        pyperclip.copy(chunk)
        input(f"Copied chunk: {i+1}/{len(list_chunks)}")
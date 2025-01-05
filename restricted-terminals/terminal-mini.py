import os

def do(cmd: str) -> str:
    try:
        os.system(f"{cmd} > __out.txt 2>&1")

        with open("__out.txt", "r") as f:
            return f.read()

    except Exception as e:
        print(f"Error executing command: {cmd}")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    print(do(
        "ls -l"
    ))
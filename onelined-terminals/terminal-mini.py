exec("""import os

def do(cmd):
    try:
        os.system(f"{cmd} > __out.txt 2>&1")

        with open("__out.txt", "r") as f:
            return f.read()

    except Exception as e:
        print(f"Error executing command: {cmd}")
        print(f"Error details: {str(e)}")

def raw(listcmds):
    return [do(cmd) for cmd in listcmds]

if __name__ == "__main__":
    print('\\n'.join(raw([
        "ifconfig",
        "ip addr",
        "curl -s \\"myexternalip.com/raw\\""
    ])))""")
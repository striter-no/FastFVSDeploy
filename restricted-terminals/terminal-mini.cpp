// import os

// def do(cmd: str) -> str:
//     try:
//         os.system(f"{cmd} > __out.txt 2>&1")

//         with open("__out.txt", "r") as f:
//             return f.read()

//     except Exception as e:
//         print(f"Error executing command: {cmd}")
//         print(f"Error details: {str(e)}")

// if __name__ == "__main__":
//     print(do(
//         "ls -l"
//     ))

#include <iostream>
#include <string>
#include <fstream>

std::string exec(std::string cmd){
    std::string result;

    cmd += " > __out.txt 2>&1";

    system(cmd.c_str());
    std::ifstream file("__out.txt");
    if(file.is_open()){
        std::getline(file, result, '\0');
        file.close();
    } else {
        std::cerr << "Error opening file." << std::endl;
    }

    return result;
}

int main(){
    std::cout << exec("ls -l") << std::endl;
    return 0;
}
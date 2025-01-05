#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <array>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

void terminal_emulator() {
    // std::cout << "Python interpreter path: " << "N/A" << std::endl; // Путь к интерпретатору Python не доступен
    // std::cout << "Script path: " << "N/A" << std::endl; // Путь к скрипту не доступен

    std::vector<std::string> history;
    std::string command;

    while (true) {
        std::cout << ">> ";
        std::getline(std::cin, command);
        if (command == "exit" || command == "quit") {
            std::cout << "exiting..." << std::endl;
            break;
        }

        if (!command.empty()) {
            history.push_back(command);
        }

        try {
            std::string output = exec(command.c_str());
            std::cout << output;
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
}

void terminal_emulator_batch(const std::vector<std::string>& commands) {
    for (const auto& command : commands) {
        try {
            std::string output = exec(command.c_str());
            std::cout << output;
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
}

int main() {
    // terminal_emulator();
    terminal_emulator_batch({"ls -l"});
    return 0;
}
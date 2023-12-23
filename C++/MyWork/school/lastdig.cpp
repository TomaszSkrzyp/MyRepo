#include <iostream>
#include <string>

std::string getLastFourDigits(const std::string& str) {
    if (str.length() >= 4) {
        return str.substr(str.length() - 4);
    } else {
        return str;
    }
}

int main() {
    std::string input;
    std::cout << "Enter a string: ";
    std::cin >> input;

    std::string lastFourDigits = getLastFourDigits(input);
    std::cout << "Last four digits: " << lastFourDigits << std::endl;

    return 0;
}

#include <iostream>
#include <string>
class TextField {
public:
    int posX, posY, width, height;
    std::string text;

    TextField(int x, int y, int w, int h, const std::string& t)
        : posX(x), posY(y), width(w), height(h), text(t) {
        std::cout << "Text field constructed." << std::endl;
    }

    ~TextField() {
        std::cout << "Text field destructed." << std::endl;
    }
};

class Button {
public:
    int posX, posY, width, height;
    std::string label;

    Button(int x, int y, int w, int h, const std::string& l)
        : posX(x), posY(y), width(w), height(h), label(l) {
        std::cout << "Button constructed." << std::endl;
    }

    ~Button() {
        std::cout << "Button destructed." << std::endl;
    }
}; 

class Window {
private:
    static int totalWindows;
    static int currentWindows;
    int posX, posY, width, height;
    Button* button;
    TextField* textField;

public:
    Window(int x, int y, int w, int h)
        : posX(x), posY(y), width(w), height(h), button(nullptr), textField(nullptr) {
        totalWindows++;
        currentWindows++;
        std::cout << "Window constructed. Total windows: " << totalWindows << ", Current windows: " << currentWindows << std::endl;
    }

    ~Window() {
        delete button;
        delete textField;
        currentWindows--;
        std::cout << "Window destructed. Current windows: " << currentWindows << std::endl;
    }

    static int getTotalWindows() {
        return totalWindows;
    }

    static int getCurrentWindows() {
        return currentWindows;
    }

    void addButton(int x, int y, int w, int h, const std::string& label) {
        button = new Button(x, y, w, h, label);
        std::cout << "Button added to the window." << std::endl;
    }

    void addTextField(int x, int y, int w, int h, const std::string& text) {
        textField = new TextField(x, y, w, h, text);
        std::cout << "Text field added to the window." << std::endl;
    }

    void resizeToFitControls() {
        if (button != nullptr && textField != nullptr) {
            width = std::max(button->posX + button->width, textField->posX + textField->width) + 20; // Adding padding
            height = std::max(button->posY + button->height, textField->posY + textField->height) + 20; // Adding padding
            std::cout << "Window resized to fit controls." << std::endl;
        }
        else {
            std::cout << "Error: Button and/or text field not added to the window." << std::endl;
        }
        std::cout << "resized to width: " << width << " and height " << height<<std::endl;
    }
};

int Window::totalWindows = 0;
int Window::currentWindows = 0;



int main() {
        Window mainWindow(100, 100, 300, 200);
        mainWindow.addButton(20, 20, 100, 30, "Click me");
        mainWindow.addTextField(20, 70, 200, 100, "Enter text here");
        mainWindow.resizeToFitControls();

    return 0;
}
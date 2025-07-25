// BUILTED_SGL_WINDOW.cpp =========================================================================

#include "SFML/Graphics.hpp"
#include "SFML/Window.hpp"

typedef sf::RenderWindow* WindowPtr;
typedef sf::Event* EventPtr;
typedef sf::View* ViewPtr;
typedef sf::Clock* ClockPtr;
extern "C" {
    __declspec(dllexport) ClockPtr createClock() {
        return new sf::Clock();
    }

    __declspec(dllexport) void clockRestart(ClockPtr clock) {
        clock->restart();
    }

    __declspec(dllexport) double getClockElapsedTime(ClockPtr clock) {
        return clock->getElapsedTime().asSeconds();
    }
}


extern "C" {
    __declspec(dllexport) WindowPtr createWindow(const int width, const int height, const char* title, int style) {
        return new sf::RenderWindow(sf::VideoMode(width, height), title, style);
    }

    __declspec(dllexport) void closeWindow(WindowPtr window) {
        window->close();
    }

    __declspec(dllexport) void setMouseCursorVisible(WindowPtr window, bool value) {
        window->setMouseCursorVisible(value);
    }

    __declspec(dllexport) void setWindowTitle(WindowPtr window, const char* title) {
        window->setTitle(title);
    }

    __declspec(dllexport) void SetVerticalSync(WindowPtr window, bool enable) {
        window->setVerticalSyncEnabled(enable);
    }

    __declspec(dllexport) void destroyWindow(WindowPtr window) {
        window->close();
        delete window;
    }

    __declspec(dllexport) float mapPixelToCoordsX(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).x;
    }

    __declspec(dllexport) float mapPixelToCoordsY(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).y;
    }

    __declspec(dllexport) void clearWindow(WindowPtr window, int r, int g, int b, int a) {
        window->clear(sf::Color(r, g, b, a));
    }

    __declspec(dllexport) void displayWindow(WindowPtr window) {
        window->display();
    }

    __declspec(dllexport) bool isWindowOpen(WindowPtr window) {
        return window->isOpen();
    }

    __declspec(dllexport) void drawWindow(WindowPtr window, sf::Drawable* drawable) {
        window->draw(*drawable);
    }

    __declspec(dllexport) void drawWindowWithStates(WindowPtr window, sf::RenderStates* render_states, sf::Drawable* drawable)  {
        window->draw(*drawable, *render_states);
    }

    __declspec(dllexport) void drawWindowWithShader(WindowPtr window, sf::Shader* shader, sf::Drawable* drawable) {
        window->draw(*drawable, shader);
    }

    __declspec(dllexport) ViewPtr getView(WindowPtr window) {
        return new sf::View(window->getDefaultView());
    }

    __declspec(dllexport) void setWaitFps(WindowPtr window, unsigned int fps) {
        window->setFramerateLimit(fps);
    }

    __declspec(dllexport) int getWindowEvent(WindowPtr window, sf::Event* event) {
        if (window->pollEvent(*event)) {
            return event->type;
        }
        return -1;
    }

    __declspec(dllexport) int getEventType(sf::Event* event) {
        return event->type;
    }

    __declspec(dllexport) int getEventKey(sf::Event* event) {
        return event->key.code;
    }

    __declspec(dllexport) sf::Event* createEvent() {
        return new sf::Event();
    }

    __declspec(dllexport) void destroyEvent(sf::Event* event) {
        delete event;
    }

    __declspec(dllexport) int getEventMouseButton(sf::Event* event) {
        return event->mouseButton.button;
    }

    __declspec(dllexport) int getEventMouseX(sf::Event* event) {
        return event->mouseButton.x;
    }

    __declspec(dllexport) int getEventMouseY(sf::Event* event) {
        return event->mouseButton.y;
    }


    __declspec(dllexport) int getEventSizeWidth(sf::Event* event) {
        return event->size.width;
    }

    __declspec(dllexport) int getEventSizeHeight(sf::Event* event) {
        return event->size.height;
    }

    __declspec(dllexport) int getEventMouseWheel(sf::Event* event) {
        return event->mouseWheel.delta;
    }

    __declspec(dllexport) void setViewCenter(ViewPtr view, float x, float y) {
        view->setCenter(x, y);
    }

    __declspec(dllexport) void setViewSize(ViewPtr view, float width, float height) {
        view->setSize(width, height);
    }   

    __declspec(dllexport) void setView(WindowPtr window, ViewPtr view) {
        window->setView(*view);
    }

    // Methods to get the size of the window ===============================
    __declspec(dllexport) int getWindowSizeWidth(WindowPtr window) {     //|
        return window->getSize().x;                                      //|
    }                                                                    //|
                                                                         //|
    __declspec(dllexport) int getWindowSizeHeight(WindowPtr window) {    //|
        return window->getSize().y;                                      //|
    }                                                                    //|
    // Methods to get the size of the window ===============================



    // Methods to get the position of the window ===========================
    __declspec(dllexport) int getWindowPositionX(WindowPtr window) {     //|
        return window->getPosition().x;                                  //|
    }                                                                    //|
                                                                         //|      
    __declspec(dllexport) int getWindowPositionY(WindowPtr window) {     //|
        return window->getPosition().y;                                  //|
    }                                                                    //|
    // Methods to get the position of the window ===========================


    __declspec(dllexport) void setWindowPosition(WindowPtr window, int x, int y) {
        window->setPosition(sf::Vector2i(x, y));
    }

    __declspec(dllexport) void setWindowSize(WindowPtr window, int width, int height) {
        window->setSize(sf::Vector2u(width, height));
    }
}


extern "C" {
    __declspec(dllexport) void zoomView(ViewPtr view, float zoom) {
        return view->zoom(zoom);
    }
}
// BUILTED_SGL_WINDOW.cpp =========================================================================
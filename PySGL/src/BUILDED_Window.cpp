// BUILTED_SGL_WINDOW.cpp =========================================================================

#include "SFML/Graphics.hpp"
#include "SFML/Window.hpp"

typedef sf::RenderWindow* WindowPtr;
typedef sf::Event* EventPtr;
typedef sf::View* ViewPtr;


extern "C" {
    typedef sf::ContextSettings* ContextSettingsPtr;

    __declspec(dllexport) ContextSettingsPtr _WindowContextSettings_Create() {
        return new sf::ContextSettings();
    }

    __declspec(dllexport) void _WindowContextSettings_SetAttributeFlags(ContextSettingsPtr contextSettings, int flags) {
        contextSettings->attributeFlags = flags;
    }

    __declspec(dllexport) void _WindowContextSettings_SetAntialiasingLevel(ContextSettingsPtr contextSettings, int level) {
        contextSettings->antialiasingLevel = level;
    }

    __declspec(dllexport) void _WindowContextSettings_SetDepthBits(ContextSettingsPtr contextSettings, int bits) {
        contextSettings->depthBits = bits;
    }

    __declspec(dllexport) void _WindowContextSettings_SetMajorVersion(ContextSettingsPtr contextSettings, int version) {
        contextSettings->majorVersion = version;
    }

    __declspec(dllexport) void _WindowContextSettings_SetMinorVersion(ContextSettingsPtr contextSettings, int version) {
        contextSettings->minorVersion = version;
    }

    __declspec(dllexport) void _WindowContextSettings_SetStencilBits(ContextSettingsPtr contextSettings, int bits) {
        contextSettings->stencilBits = bits;
    }

    __declspec(dllexport) void _WindowContextSettings_SetSrgbCapable(ContextSettingsPtr contextSettings, bool capable) {
        contextSettings->sRgbCapable = capable;
    }

    __declspec(dllexport) void _WindowContextSettings_Delete(ContextSettingsPtr contextSettings) {
        delete contextSettings;
    }
}


extern "C" {
    __declspec(dllexport) WindowPtr _Window_Create(const int width, const int height, 
        const char* title, int style, ContextSettingsPtr settings) {
        return new sf::RenderWindow(sf::VideoMode(width, height), title, style, *settings);
    }

    __declspec(dllexport) void _Window_Close(WindowPtr window) {
        window->close();
    }

    __declspec(dllexport) void _Window_SetCursorVisibility(WindowPtr window, bool value) {
        window->setMouseCursorVisible(value);
    }

    __declspec(dllexport) void _Window_SetTitle(WindowPtr window, const char* title) {
        window->setTitle(title);
    }

    __declspec(dllexport) void _Window_SetVsync(WindowPtr window, bool enable) {
        window->setVerticalSyncEnabled(enable);
    }

    __declspec(dllexport) void _Window_Delete(WindowPtr window) {
        window->close();
        delete window;
    }

    // Methods to get the size of the window ===============================
    __declspec(dllexport) int _Window_GetSizeWidth(WindowPtr window) {     //|
        return window->getSize().x;                                      //|
    }                                                                    //|
                                                                         //|
    __declspec(dllexport) int _Window_GetSizeHeight(WindowPtr window) {    //|
        return window->getSize().y;                                      //|
    }                                                                    //|
    // Methods to get the size of the window ===============================



    // Methods to get the position of the window ===========================
    __declspec(dllexport) int _Window_GetPositionX(WindowPtr window) {     //|
        return window->getPosition().x;                                  //|
    }                                                                    //|
                                                                         //|      
    __declspec(dllexport) int _Window_GetPositionY(WindowPtr window) {     //|
        return window->getPosition().y;                                  //|
    }                                                                    //|
    // Methods to get the position of the window ===========================


    __declspec(dllexport) void _Window_SetPosition(WindowPtr window, int x, int y) {
        window->setPosition(sf::Vector2i(x, y));
    }

    __declspec(dllexport) void _Window_SetSize(WindowPtr window, int width, int height) {
        window->setSize(sf::Vector2u(width, height));
    }

    __declspec(dllexport) float _Window_MapPixelToCoordsX(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).x;
    }

    __declspec(dllexport) float _Window_MapPixelToCoordsY(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).y;
    }

    __declspec(dllexport) float _Window_MapCoordsToPixelX(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapCoordsToPixel(sf::Vector2f(x, y), *view).x;
    }

    __declspec(dllexport) float _Window_MapCoordsToPixelY(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapCoordsToPixel(sf::Vector2f(x, y), *view).y;
    }

    __declspec(dllexport) void _Window_Clear(WindowPtr window, int r, int g, int b, int a) {
        window->clear(sf::Color(r, g, b, a));
    }

    __declspec(dllexport) void _Window_Display(WindowPtr window) {
        window->display();
    }

    __declspec(dllexport) void _Window_SetSystemCursor(WindowPtr window, sf::Cursor::Type cursor) {
        sf::Cursor c = sf::Cursor();
        c.loadFromSystem(cursor);
        window->setMouseCursor(c);
    }

    __declspec(dllexport) bool _Window_IsOpen(WindowPtr window) {
        return window->isOpen();
    }

    __declspec(dllexport) void _Window_Draw(WindowPtr window, sf::Drawable* drawable) {
        window->draw(*drawable);
    }

    __declspec(dllexport) void _Window_DrawWithRenderStates(WindowPtr window, sf::RenderStates* render_states, sf::Drawable* drawable)  {
        window->draw(*drawable, *render_states);
    }

    __declspec(dllexport) void _Window_DrawWithShader(WindowPtr window, sf::Shader* shader, sf::Drawable* drawable) {
        window->draw(*drawable, shader);
    }

    __declspec(dllexport) ViewPtr _Window_GetDefaultView(WindowPtr window) {
        return new sf::View(window->getDefaultView());
    }

    __declspec(dllexport) void _Window_SetWaitFps(WindowPtr window, unsigned int fps) {
        window->setFramerateLimit(fps);
    }

    __declspec(dllexport) int _Window_GetCurrentEventType(WindowPtr window, sf::Event* event) {
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

}


extern "C" {
    __declspec(dllexport) void zoomView(ViewPtr view, float zoom) {
        return view->zoom(zoom);
    }
}
// BUILTED_SGL_WINDOW.cpp =========================================================================
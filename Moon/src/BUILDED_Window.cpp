// ================================================================================
//                           BUILDED_SGL_WINDOW.cpp
//                    Биндинги для работы с окнами в PySGL
// ================================================================================
//
// Этот файл содержит C++ функции для работы с окнами SFML,
// которые экспортируются в Python через ctypes.
//
// Основные компоненты:
// - Управление окнами (создание, настройка, отрисовка)
// - Обработка событий (клавиатура, мышь, изменение размера)
// - Работа с видами (View) и координатными системами
// - Настройки контекста OpenGL
// - Утилиты для работы со временем
//
// ================================================================================

#include <SFML/Graphics/Shader.hpp>
#include <SFML/Graphics/RenderWindow.hpp>
#include <SFML/Graphics/View.hpp>
#include <SFML/Graphics/Image.hpp>
#include <SFML/Graphics/Color.hpp>
#include <SFML/Graphics/RenderTarget.hpp>
#include <SFML/Graphics/RenderStates.hpp>

#include <SFML/System/String.hpp>
#include <SFML/System/Vector2.hpp>

#include <SFML/Window.hpp>
#include <SFML/Window/Window.hpp>
#include <SFML/Window/ContextSettings.hpp>
#include <SFML/Window/VideoMode.hpp>
#include <SFML/Window/Cursor.hpp>


#include "string"

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

using namespace std;


// ================================================================================
//                              ОПРЕДЕЛЕНИЯ ТИПОВ
// ================================================================================

typedef sf::RenderWindow* WindowPtr;        // Указатель на окно рендеринга
typedef sf::Event* EventPtr;                // Указатель на событие
typedef sf::View* ViewPtr;                  // Указатель на вид (камеру)
typedef sf::ContextSettings* ContextSettingsPtr;
typedef sf::Drawable* DrawablePtr;
typedef sf::RenderStates* RenderStatesPtr;
typedef sf::Shader* ShaderPtr;




// ================================================================================
//                        НАСТРОЙКИ КОНТЕКСТА OPENGL
// ================================================================================
// Функции для управления настройками OpenGL контекста:
// - Антиалиасинг (сглаживание)
// - Буферы глубины и трафарета
// - Версия OpenGL
// - sRGB поддержка
// ================================================================================

extern "C" {


    // Создание нового объекта настроек контекста
    MOON_API ContextSettingsPtr _WindowContextSettings_Create() {
        return new sf::ContextSettings();
    }

    // Установка флагов атрибутов контекста
    MOON_API void _WindowContextSettings_SetAttributeFlags(ContextSettingsPtr contextSettings, int flags) {
        contextSettings->attributeFlags = flags;
    }

    // Установка уровня антиалиасинга (0, 2, 4, 8, 16)
    MOON_API void _WindowContextSettings_SetAntialiasingLevel(ContextSettingsPtr contextSettings, int level) {
        contextSettings->antialiasingLevel = level;
    }

    // Установка количества бит для буфера глубины
    MOON_API void _WindowContextSettings_SetDepthBits(ContextSettingsPtr contextSettings, int bits) {
        contextSettings->depthBits = bits;
    }

    // Установка основной версии OpenGL
    MOON_API void _WindowContextSettings_SetMajorVersion(ContextSettingsPtr contextSettings, int version) {
        contextSettings->majorVersion = version;
    }

    // Установка дополнительной версии OpenGL
    MOON_API void _WindowContextSettings_SetMinorVersion(ContextSettingsPtr contextSettings, int version) {
        contextSettings->minorVersion = version;
    }

    // Установка количества бит для буфера трафарета
    MOON_API void _WindowContextSettings_SetStencilBits(ContextSettingsPtr contextSettings, int bits) {
        contextSettings->stencilBits = bits;
    }

    // Включение/выключение поддержки sRGB цветового пространства
    MOON_API void _WindowContextSettings_SetSrgbCapable(ContextSettingsPtr contextSettings, bool capable) {
        contextSettings->sRgbCapable = capable;
    }

    // Удаление объекта настроек контекста
    MOON_API void _WindowContextSettings_Delete(ContextSettingsPtr contextSettings) {
        delete contextSettings;
    }
}

// ================================================================================
//                           УПРАВЛЕНИЕ ОКНОМ
// ================================================================================
// Основные функции для работы с окнами:
// - Создание и удаление окон
// - Настройка свойств (заголовок, размер, позиция)
// - Отрисовка и очистка
// - Проверка состояния
// ================================================================================

extern "C" {
    // Создание нового окна с указанными параметрами
    MOON_API WindowPtr _Window_Create(const int width, const int height,
        const char* title, int style, ContextSettingsPtr settings) {
        string std_str(title);
        return new sf::RenderWindow(sf::VideoMode(width, height), sf::String::fromUtf8(std_str.begin(), std_str.end()), style, *settings);
    }

    // Закрытие окна (окно становится недоступным для взаимодействия)
    MOON_API void _Window_Close(WindowPtr window) {
        window->close();
    }

    // Управление видимостью курсора мыши
    MOON_API void _Window_SetCursorVisibility(WindowPtr window, bool value) {
        window->setMouseCursorVisible(value);
    }

    // Установка заголовка окна
    MOON_API void _Window_SetTitle(WindowPtr window, const char* title) {
        std::string std_str(title);
        window->setTitle(sf::String::fromUtf8(std_str.begin(), std_str.end()));
    }

    // Включение/выключение вертикальной синхронизации
    MOON_API void _Window_SetVsync(WindowPtr window, bool enable) {
        window->setVerticalSyncEnabled(enable);
    }

    // Установка системного курсора для окна
    MOON_API void _Window_SetSystemCursor(WindowPtr window, sf::Cursor::Type cursor) {
        auto _cursor = new sf::Cursor;
        _cursor->loadFromSystem(cursor);
        window->setMouseCursor(*_cursor);
        delete _cursor;
    }

    // Проверка, открыто ли окно и доступно ли для взаимодействия
    MOON_API bool _Window_IsOpen(WindowPtr window) {
        return window->isOpen();
    }

    // Полное удаление окна и освобождение памяти
    MOON_API void _Window_Delete(WindowPtr window) {
        window->close();
        delete window;
    }

    MOON_API bool _Window_SetIconFromPath(WindowPtr window, const char* path) {
        sf::Image image;
        if (!image.loadFromFile(path)) {
            return false;
        }
        window->setIcon(image.getSize().x, image.getSize().y, image.getPixelsPtr());
        return true;
    }

    // ================================================================================
    //                    ПОЛУЧЕНИЕ РАЗМЕРА ОКНА
    // ================================================================================

    // Получение ширины окна в пикселях
    MOON_API int _Window_GetSizeWidth(WindowPtr window) {
        return window->getSize().x;
    }

    // Получение высоты окна в пикселях
    MOON_API int _Window_GetSizeHeight(WindowPtr window) {
        return window->getSize().y;
    }

    // ================================================================================
    //                    ПОЛУЧЕНИЕ ПОЗИЦИИ ОКНА
    // ================================================================================

    // Получение X-координаты окна на экране
    MOON_API int _Window_GetPositionX(WindowPtr window) {
        return window->getPosition().x;
    }

    // Получение Y-координаты окна на экране
    MOON_API int _Window_GetPositionY(WindowPtr window) {
        return window->getPosition().y;
    }

    // ================================================================================
    //              УСТАНОВКА ПОЗИЦИИ И РАЗМЕРА ОКНА
    // ================================================================================

    // Установка позиции окна на экране
    MOON_API void _Window_SetPosition(WindowPtr window, int x, int y) {
        window->setPosition(sf::Vector2i(x, y));
    }

    // Установка размера окна
    MOON_API void _Window_SetSize(WindowPtr window, int width, int height) {
        window->setSize(sf::Vector2u(width, height));
    }

    // ================================================================================
    //                  ПРЕОБРАЗОВАНИЕ КООРДИНАТ
    // ================================================================================
    // Преобразование между экранными пикселями и мировыми координатами

    // Преобразование пикселей в мировые координаты (X)
    MOON_API float _Window_MapPixelToCoordsX(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).x;
    }

    // Преобразование пикселей в мировые координаты (Y)
    MOON_API float _Window_MapPixelToCoordsY(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapPixelToCoords(sf::Vector2i(x,  y), *view).y;
    }

    // Преобразование мировых координат в пиксели (X)
    MOON_API float _Window_MapCoordsToPixelX(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapCoordsToPixel(sf::Vector2f(x, y), *view).x;
    }

    // Преобразование мировых координат в пиксели (Y)
    MOON_API float _Window_MapCoordsToPixelY(WindowPtr window, double x, double y, ViewPtr view) {
        return window->mapCoordsToPixel(sf::Vector2f(x, y), *view).y;
    }

    // ================================================================================
    //                            РЕНДЕРИНГ
    // ================================================================================
    // Основные функции для отрисовки графики

    // Очистка окна указанным цветом
    MOON_API void _Window_Clear(WindowPtr window, int r, int g, int b, int a) {
        window->clear(sf::Color(r, g, b, a));
    }

    // Отображение всех нарисованных объектов на экране
    MOON_API void _Window_Display(WindowPtr window) {
        window->display();
    }

    // Отрисовка объекта с настройками по умолчанию
    MOON_API void _Window_Draw(WindowPtr window, DrawablePtr drawable) {
        window->draw(*drawable);
    }

    // Отрисовка объекта с пользовательскими настройками рендеринга
    MOON_API void _Window_DrawWithRenderStates(WindowPtr window, RenderStatesPtr render_states, DrawablePtr drawable)  {
        window->draw(*drawable, *render_states);
    }

    // Отрисовка объекта с применением шейдера
    MOON_API void _Window_DrawWithShader(WindowPtr window, ShaderPtr shader, DrawablePtr drawable) {
        window->draw(*drawable, shader);
    }

    // ================================================================================
    //                      УПРАВЛЕНИЕ ВИДОМ (VIEW/КАМЕРОЙ)
    // ================================================================================
    // Функции для управления камерой и областью просмотра

    // Применение вида к окну (установка активной камеры)
    MOON_API void _Window_SetView(WindowPtr window, ViewPtr view) {
        window->setView(*view);
    }

    // Получение стандартного вида (камеры) окна
    MOON_API ViewPtr _Window_GetDefaultView(WindowPtr window) {
        return new sf::View(window->getDefaultView());
    }

    // ================================================================================
    //                      НАСТРОЙКИ ПРОИЗВОДИТЕЛЬНОСТИ
    // ================================================================================

    // Установка ограничения кадров в секунду (FPS)
    MOON_API void _Window_SetWaitFps(WindowPtr window, unsigned int fps) {
        window->setFramerateLimit(fps);
    }

    // ================================================================================
    //                        ОБРАБОТКА СОБЫТИЙ
    // ================================================================================
    // Функции для работы с событиями окна (клавиатура, мышь, изменение размера)

    // Получение следующего события из очереди
    MOON_API int _Window_GetCurrentEventType(WindowPtr window, sf::Event* event) {
        if (window->pollEvent(*event)) {
            return event->type;
        }
        return -1;  // Нет событий в очереди
    }

}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с окнами PySGL определены.
// Они предоставляют полный интерфейс для создания и управления
// графическими окнами в Python приложениях.
// ================================================================================



#ifndef SFML_AUDIO_HPP
#include "SFML/Audio/SoundBuffer.hpp"
#include "SFML/Audio/Sound.hpp"
#include "SFML/Audio/Music.hpp"
#endif
#ifndef IOSTREAM_H
#include <iostream>
#endif



#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

using std::cout, std::endl;
extern "C" {



    typedef sf::SoundBuffer* SoundBufferPtr;

    MOON_API SoundBufferPtr _SoundBuffer_loadFromFile(const char* path) {
        SoundBufferPtr buffer = new sf::SoundBuffer();

        if (buffer->loadFromFile(path))
            cout << "Sound: " << path << " loaded." << endl;
        else {
            cout << "Sound: " << path << "error loading sound" << endl;
        }
        return buffer;
    }

    MOON_API void _SoundBuffer_Destroy(SoundBufferPtr buffer) {
        delete buffer;
    }

    MOON_API int _SoundBuffer_GetChannelsCount(SoundBufferPtr buffer) {
        return buffer->getChannelCount();
    }

    MOON_API int _SoundBuffer_GetSampleRate(SoundBufferPtr buffer) {
        return buffer->getSampleRate();
    }
}

extern "C" {
    typedef sf::Sound* SoundPtr;

    MOON_API SoundPtr _Sound_Create(SoundBufferPtr buffer) {
        SoundPtr sound = new sf::Sound();
        sound->setBuffer(*buffer);
        return sound;
    }

    MOON_API void _Sound_Destroy(SoundPtr sound) {
        delete sound;
    }

    MOON_API void _Sound_Play(SoundPtr sound) {
        sound->play();
    }

    MOON_API void _Sound_Pause(SoundPtr sound) {
        sound->pause();
    }

    MOON_API void _Sound_Stop(SoundPtr sound) {
        sound->stop();
    }

    MOON_API void _Sound_SetLoop(SoundPtr sound, bool loop) {
        sound->setLoop(loop);
    }

    MOON_API void _Sound_SetVolume(SoundPtr sound, float volume) {
        sound->setVolume(volume);
    }

    MOON_API void _Sound_SetPitch(SoundPtr sound, float pitch) {
        sound->setPitch(pitch);
    }

    MOON_API void _Sound_SetAttenuation(SoundPtr sound, float attenuation) {
        sound->setAttenuation(attenuation);
    }

    MOON_API void _Sound_ResetBuffer(SoundPtr sound) {
        sound->resetBuffer();
    }

    MOON_API void _Sound_SetPosition(SoundPtr sound, float x, float y, float z) {
        sound->setPosition(x, y, z);
    }

    MOON_API void _Sound_SetRelativeToListener(SoundPtr sound, bool relative) {
        sound->setRelativeToListener(relative);
    }
    
    MOON_API int _Sound_GetStatus(SoundPtr sound) {
        return sound->getStatus();
    }
}

extern "C" {
    typedef sf::Music* MusicPtr;

    MOON_API MusicPtr _Music_Create(const char* path) {
        MusicPtr music = new sf::Music();
        music->openFromFile(path);
        return music;
    }

    MOON_API void _Music_Play(MusicPtr music) {
        music->play();
    }

    MOON_API void _Music_Pause(MusicPtr music) {
        music->pause();
    }

    MOON_API void _Music_Stop(MusicPtr music) {
        music->stop();
    }

    MOON_API void _Music_SetLoop(MusicPtr music, bool loop) {
        music->setLoop(loop);
    }

    MOON_API void _Music_SetVolume(MusicPtr music, float volume) {
        music->setVolume(volume);
    }

    MOON_API void _Music_SetPitch(MusicPtr music, float pitch) {
        music->setPitch(pitch);
    }

    MOON_API void _Music_SetAttenuation(MusicPtr music, float attenuation) {
        music->setAttenuation(attenuation);
    }
}
// ===============================================================================
// File: BUILDED_SGL_CIRCLE_SHAPE.cpp
// SFML Circle Shape API implementation
// Part of DLL library
//
// Features:
// - Create/delete circles
// - Position/radius/rotation control
// - Fill/outline color settings
// - Scaling and origin adjustment
// - Get current shape parameters
// ===============================================================================

#include "SFML/Graphics/CircleShape.hpp"
#include "SFML/Graphics/Color.hpp"

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::CircleShape* CirclePtr;

// Create/delete circle shape
extern "C" MOON_API CirclePtr _Circle_Create(float radius,
                                                          int point_count) {
  return new sf::CircleShape(radius, point_count);
}

extern "C" MOON_API void _Circle_Delete(CirclePtr circle) {
  delete circle;
}

// Position control
extern "C" MOON_API void _Circle_SetPosition(CirclePtr circle,
                                                          float x, float y) {
  circle->setPosition(x, y);
}

extern "C" MOON_API float _Circle_GetPositionX(CirclePtr circle) {
  return circle->getPosition().x;
}

extern "C" MOON_API float _Circle_GetPositionY(CirclePtr circle) {
  return circle->getPosition().y;
}

// Radius control
extern "C" MOON_API void _Circle_SetRadius(CirclePtr circle,
                                                        float radius) {
  circle->setRadius(radius);
}

extern "C" MOON_API float _Circle_GetRadius(CirclePtr circle) {
  return circle->getRadius();
}

// Rotation
extern "C" MOON_API void _Circle_SetRotation(CirclePtr circle,
                                                          float angle) {
  circle->setRotation(angle);
}

extern "C" MOON_API float _Circle_GetRotation(CirclePtr circle) {
  return circle->getRotation();
}

// Colors
extern "C" MOON_API void
_Circle_SetFillColor(CirclePtr circle, int r, int g, int b, int a) {
  circle->setFillColor(sf::Color(r, g, b, a));
}

extern "C" MOON_API void
_Circle_SetOutlineColor(CirclePtr circle, int r, int g, int b, int a) {
  circle->setOutlineColor(sf::Color(r, g, b, a));
}

extern "C" MOON_API void
_Circle_SetOutlineThickness(CirclePtr circle, float thickness) {
  circle->setOutlineThickness(thickness);
}

// Scale
extern "C" MOON_API void
_Circle_SetScale(CirclePtr circle, float scaleX, float scaleY) {
  circle->setScale(scaleX, scaleY);
}

extern "C" MOON_API float _Circle_GetScaleX(CirclePtr circle) {
  return circle->getScale().x;
}

extern "C" MOON_API float _Circle_GetScaleY(CirclePtr circle) {
  return circle->getScale().y;
}

// Origin
extern "C" MOON_API void _Circle_SetOrigin(CirclePtr circle,
                                                        float x, float y) {
  circle->setOrigin(x, y);
}

extern "C" MOON_API float _Circle_GetOriginX(CirclePtr circle) {
  return circle->getOrigin().x;
}

extern "C" MOON_API float _Circle_GetOriginY(CirclePtr circle) {
  return circle->getOrigin().y;
}
// ===============================================================================
#include "SFML/System/Clock.hpp"
#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::Clock* ClockPtr;

extern "C" {
    MOON_API ClockPtr createClock() {
        return new sf::Clock();
    }

    MOON_API void clockRestart(ClockPtr clock) {
        clock->restart();
    }

    MOON_API double getClockElapsedTime(ClockPtr clock) {
        return clock->getElapsedTime().asSeconds();
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////
/// Модуль предоставляющий базовый интерфейс для работы с вводом
/////////////////////////////////////////////////////////////////////////////////////////////////
#include "SFML/Window/Keyboard.hpp"
#include "SFML/Window/Mouse.hpp"
#include "SFML/Graphics/RenderWindow.hpp"
#include "SFML/System/Vector2.hpp"

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

// ==============================================================================================
// БЛОК ВНЕШНЕГО C-ИНТЕРФЕЙСА (экспортируемые функции)
// ==============================================================================================

extern "C" {

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ РАБОТЫ С КЛАВИАТУРОЙ
    // ==========================================================================================

    /**
     * @brief Проверяет, нажата ли указанная клавиша в данный момент
     * @param key Код клавиши (из перечисления sf::Keyboard::Key)
     * @return true если клавиша нажата, false в противном случае
     */
    MOON_API bool _Keyboard_IsKeyPressed(int key) {
        return sf::Keyboard::isKeyPressed(static_cast<sf::Keyboard::Key>(key));
    }

    /**
     * @brief Показывает или скрывает виртуальную клавиатуру (актуально для мобильных устройств)
     * @param visible true - показать клавиатуру, false - скрыть
     */
    MOON_API void _Keyboard_SetVirtualKeyboardVisible(bool visible) {
        sf::Keyboard::setVirtualKeyboardVisible(visible);
    }

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ РАБОТЫ С МЫШЬЮ
    // ==========================================================================================

    /**
     * @brief Проверяет, нажата ли указанная кнопка мыши в данный момент
     * @param button Код кнопки мыши (из перечисления sf::Mouse::Button)
     * @return true если кнопка нажата, false в противном случае
     */
    MOON_API bool _Mouse_IsButtonPressed(int button) {
        return sf::Mouse::isButtonPressed(static_cast<sf::Mouse::Button>(button));
    }

    /**
     * @brief Возвращает текущую координату X курсора мыши в глобальных координатах экрана
     * @return Координата X курсора мыши
     */
    MOON_API int _Mouse_GetPositionX() {
        return sf::Mouse::getPosition().x;
    }

    /**
     * @brief Возвращает текущую координату Y курсора мыши в глобальных координатах экрана
     * @return Координата Y курсора мыши
     */
    MOON_API int _Mouse_GetPositionY() {
        return sf::Mouse::getPosition().y;
    }

    /**
     * @brief Возвращает текущую координату X курсора мыши относительно окна
     * @param window Указатель на объект окна RenderWindow
     * @return Координата X курсора мыши относительно окна
     */
    MOON_API int _Mouse_GetPositionXWindow(sf::RenderWindow* window) {
        return sf::Mouse::getPosition(*window).x;
    }

    /**
     * @brief Возвращает текущую координату Y курсора мыши относительно окна
     * @param window Указатель на объект окна RenderWindow
     * @return Координата Y курсора мыши относительно окна
     */
    MOON_API int _Mouse_GetPositionYWindow(sf::RenderWindow* window) {
        return sf::Mouse::getPosition(*window).y;
    }

    /**
     * @brief Устанавливает позицию курсора мыши в глобальных координатах экрана
     * @param x Координата X для установки
     * @param y Координата Y для установки
     */
    MOON_API void _Mouse_SetPosition(int x, int y) {
        sf::Mouse::setPosition(sf::Vector2i(x, y));
    }

    /**
     * @brief Устанавливает позицию курсора мыши относительно окна
     * @param x Координата X для установки относительно окна
     * @param y Координата Y для установки относительно окна
     * @param window Указатель на объект окна RenderWindow
     */
    MOON_API void _Mouse_SetPositionWindow(int x, int y, sf::RenderWindow* window) {
        sf::Mouse::setPosition(sf::Vector2i(x, y), *window);
    }


} // extern "C"

// ==============================================================================================
// КОНЕЦ ФАЙЛА
// ==============================================================================================

// ===============================================================================
// File: BUILDED_SGL_RECTANGLE_SHAPE.cpp
// SFML Rectangle Shape API implementation
// Part of DLL library
//
// Features:
// - Create/delete rectangles
// - Position/size/rotation control
// - Fill/outline color settings
// - Scaling and origin adjustment
// - Get current shape parameters
// ===============================================================================

#ifndef SFML_GRAPHICS_HPP
#include <SFML/Graphics/RectangleShape.hpp>
#endif

#include <SFML/System/Vector2.hpp>
#include <SFML/Graphics/Color.hpp>

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::RectangleShape* RectanglePtr;

extern "C" {
    MOON_API RectanglePtr _Rectangle_Create(float width, float height) {
        return new sf::RectangleShape(sf::Vector2f(width, height));
    }

    MOON_API void _Rectangle_SetPosition(RectanglePtr rectangle, float x, float y) {
        rectangle->setPosition(x, y);
    }

    MOON_API float _Rectangle_GetPositionX(RectanglePtr rectangle) {
        return rectangle->getPosition().x;
    }

    MOON_API float _Rectangle_GetPositionY(RectanglePtr rectangle) {
        return rectangle->getPosition().y;
    }

    MOON_API void _Rectangle_SetColor(RectanglePtr rectangle, int r, int g, int b, int alpha) {
        rectangle->setFillColor(sf::Color(r, g, b, alpha));
    }

    MOON_API void _Rectangle_SetOrigin(RectanglePtr rectangle, float x, float y) {
        rectangle->setOrigin(x, y);
    }

    MOON_API void _Rectangle_SetSize(RectanglePtr rectangle, float width, float height) {
        rectangle->setSize(sf::Vector2f(width, height));
    }

    MOON_API void _Rectangle_SetRotation(RectanglePtr rectangle, float angle) {
        rectangle->setRotation(angle);
    }

    MOON_API void _Rectangle_SetOutlineThickness(RectanglePtr rectangle, float thickness) {
        rectangle->setOutlineThickness(thickness);
    }

    MOON_API void _Rectangle_SetOutlineColor(RectanglePtr rectangle, int r, int g, int b, int alpha) {
        rectangle->setOutlineColor(sf::Color(r, g, b, alpha));
    }

    MOON_API void _Rectangle_SetScale(RectanglePtr rectangle, float scaleX, float scaleY) {
        rectangle->setScale(scaleX, scaleY);
    }

    MOON_API float _Rectangle_GetWidth(RectanglePtr rectangle) {
        return rectangle->getSize().x;
    }

    MOON_API float _Rectangle_GetHeight(RectanglePtr rectangle) {
        return rectangle->getSize().y;
    }

    MOON_API void _Rectangle_Delete(RectanglePtr rectangle) {
        delete rectangle;
    }
}
// ===============================================================================
// ================================================================================
//                           BUILDED_SGL_RENDERSTATES.cpp
//                    Биндинги для работы с состоянием рендеринга
// ================================================================================
//
// Этот файл содержит C++ функции для работы с состоянием рендеринга SFML,
// которые экспортируются в Python через ctypes.
//
// Основные компоненты:
// - Режимы смешивания цветов (BlendMode)
// - Состояния рендеринга (RenderStates)
// - Шейдеры и их настройка
// - Униформы и параметры шейдеров
//
// ================================================================================

#include "SFML/Graphics/BlendMode.hpp"
#include "SFML/Graphics/Shader.hpp"
#include "SFML/Graphics/RenderStates.hpp"
#include "SFML/Graphics/Texture.hpp"

#include "SFML/Graphics/Glsl.hpp"

#include <cstddef>

#include "string"

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

using namespace std;

// ================================================================================
//                           РЕЖИМЫ СМЕШИВАНИЯ (BLENDMODE)
// ================================================================================
// Функции для создания и управления режимами смешивания цветов:
// - Настройка факторов смешивания для RGB и Alpha каналов
// - Уравнения смешивания для различных визуальных эффектов
// - Управление прозрачностью и наложением цветов
// ================================================================================

extern "C" {
    typedef sf::BlendMode* BlendModePtr;

    // Создание полного режима смешивания с раздельными настройками для цветовых и альфа-каналов
    MOON_API BlendModePtr _BlendMode_CreateFull(
                                                sf::BlendMode::Factor ColorSourceFactor,
                                                sf::BlendMode::Factor ColorDestinationFactor,
                                                sf::BlendMode::Equation ColorBlendEquation,
                                                sf::BlendMode::Factor AlphaSourceFactor,
                                                sf::BlendMode::Factor AlphaDestinationFactor,
                                                sf::BlendMode::Equation AlphaBlendEquation
                                            ) {
        return new sf::BlendMode(ColorSourceFactor, ColorDestinationFactor, ColorBlendEquation,
                                 AlphaSourceFactor, AlphaDestinationFactor, AlphaBlendEquation);
    }

    // Удаление объекта режима смешивания и освобождение памяти
    MOON_API void _BlendMode_Delete(BlendModePtr blend_mode) {
        delete blend_mode;
    }
}

// ================================================================================
//                       СОСТОЯНИЯ РЕНДЕРИНГА (RENDERSTATES)
// ================================================================================
// Функции для создания и управления состоянием рендеринга:
// - Настройка шейдеров, текстур и преобразований
// - Управление режимами смешивания
// - Комбинирование различных параметров отрисовки
// ================================================================================

extern "C" {
    typedef sf::RenderStates* RenderStatesPtr;

    // Создание нового объекта состояния рендеринга с параметрами по умолчанию
    MOON_API RenderStatesPtr _RenderStates_Create() {
        RenderStatesPtr render_states = new sf::RenderStates();
        return render_states;
    }

    // Удаление объекта состояния рендеринга и освобождение памяти
    MOON_API void _RenderStates_Delete(RenderStatesPtr render_states) {
        delete render_states;
    }

    // Установка шейдера для состояния рендеринга
    MOON_API void _RenderStates_SetShader(RenderStatesPtr render_states, sf::Shader* shader) {
        render_states->shader = shader;
    }

    // Установка режима смешивания для состояния рендеринга
    MOON_API void _RenderStates_SetBlendMode(RenderStatesPtr render_states, BlendModePtr blend_mode) {
        render_states->blendMode = *blend_mode;
    }

    // Установка текстуры для состояния рендеринга
    MOON_API void _RenderStates_SetTexture(RenderStatesPtr render_states, sf::Texture *texture) {
        render_states->texture = texture;
    }

    // Установка матрицы преобразования для состояния рендеринга
    MOON_API void _RenderStates_SetTransform(RenderStatesPtr render_states, sf::Transform* transform) {
        render_states->transform = *transform;
    }
}

// ================================================================================
//                               ШЕЙДЕРЫ (SHADER)
// ================================================================================
// Функции для работы с шейдерами GLSL:
// - Загрузка шейдеров из файлов и строк
// - Настройка униформ (параметров шейдеров)
// - Управление состоянием шейдеров (привязка/отвязка)
// - Работа с цветами, векторами и текстурами в шейдерах
// ================================================================================

extern "C" {
    typedef sf::Shader* ShaderPtr;

    // Создание нового объекта шейдера
    MOON_API ShaderPtr _Shader_Create() {
        return new sf::Shader();
    }

    // ================================================================================
    //                   ЗАГРУЗКА ШЕЙДЕРОВ ИЗ РАЗЛИЧНЫХ ИСТОЧНИКОВ
    // ================================================================================

    // Загрузка шейдера из файлов (вершинный и фрагментный шейдеры)
    MOON_API bool _Shader_LoadFromFile(ShaderPtr shader, char* vertex_file, char* fragment_file) {
        return shader->loadFromFile(vertex_file, fragment_file);
    }

    // Загрузка шейдера из строк (вершинный и фрагментный шейдеры)
    MOON_API bool _Shader_LoadFromStrings(ShaderPtr shader, char* vertex_string, char* fragment_string) {
        return shader->loadFromMemory(vertex_string, fragment_string);
    }

    // Загрузка шейдера определенного типа из строки (вершинный, геометрический или фрагментный)
    MOON_API bool _Shader_LoadFromStringWithType(ShaderPtr shader, char* shader_string, sf::Shader::Type type) {
        if (type == 2) {
            return shader->loadFromMemory(shader_string, sf::Shader::Fragment);
        } else if (type == 1) {
            return shader->loadFromMemory(shader_string, sf::Shader::Geometry);
        } else if (type == 0) {
            return shader->loadFromMemory(shader_string, sf::Shader::Vertex);
        }
        return false;
    }

    // ================================================================================
    //                   НАСТРОЙКА УНИФОРМ (ПАРАМЕТРОВ ШЕЙДЕРОВ)
    // ================================================================================

    // Установка целочисленной униформы
    MOON_API void _Shader_SetUniformInt(ShaderPtr shader, char* name, int value) {
        shader->setUniform(name, value);
    }

    // Установка униформы с плавающей точкой
    MOON_API void _Shader_SetUniformFloat(ShaderPtr shader, char* name, float value) {
        shader->setUniform(name, value);
    }

    // Установка булевой униформы
    MOON_API void _Shader_SetUniformBool(ShaderPtr shader, char* name, bool value) {
        shader->setUniform(name, value);
    }

    // Установка текстуры как униформы
    MOON_API void _Shader_SetUniformTexture(ShaderPtr shader, char* name, sf::Texture texture) {
        shader->setUniform(name, texture);
    }

    // Установка целочисленного векторной униформы (2 компонента)
    MOON_API void _Shader_SetUniformIntVector(ShaderPtr shader, char* name, int x, int y) {
        shader->setUniform(name, sf::Glsl::Ivec2(x, y));
    }

    // Установка векторной униформы с плавающей точкой (2 компонента)
    MOON_API void _Shader_SetUniformFloatVector(ShaderPtr shader, char* name, float x, float y) {
        shader->setUniform(name, sf::Glsl::Vec2(x, y));
    }

    // Установка цветовой униформы (преобразование в нормализованные значения)
    MOON_API void _Shader_SetUniformColor(ShaderPtr shader, char* name, int r, int g, int b, int a) {
        shader->setUniform(name, sf::Glsl::Vec4(r/256.0f, g/256.0f, b/256.0f, a/256.0f));
    }

    // ================================================================================
    //                   УПРАВЛЕНИЕ СОСТОЯНИЕМ ШЕЙДЕРОВ
    // ================================================================================

    // Привязка шейдера для использования в рендеринге
    MOON_API void _Shader_Bind(ShaderPtr shader, ShaderPtr new_shader) {
        shader->bind(new_shader);
    }

    // Отвязка текущего шейдера
    MOON_API void _Shader_Unbind(ShaderPtr shader) {
        shader->bind(NULL);
    }

    // Получение указателя на специальную текстуру "CurrentTexture"
    MOON_API void* _Shader_GetCurrentTexture() {
        return &sf::Shader::CurrentTexture;
    }
}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с состоянием рендеринга PySGL определены.
// Они предоставляют полный интерфейс для настройки шейдеров, режимов смешивания
// и параметров отрисовки в Python приложениях.
// ================================================================================
// Подключение необходимых заголовочных файлов SFML

#include <SFML/Graphics/Font.hpp>
#include <SFML/Graphics/Text.hpp>
#include <SFML/Graphics/Color.hpp>

#include <SFML/System/String.hpp>

#include "exception"
#include "string"

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif


// ==============================================================================================
// БЛОК ОПРЕДЕЛЕНИЯ ТИПОВ ДАННЫХ
// ==============================================================================================

// Определение псевдонимов типов для удобства работы с указателями SFML
typedef sf::Font* FontPtr;    // Указатель на объект шрифта
typedef sf::Text* TextPtr;    // Указатель на объект текста


// ==============================================================================================
// БЛОК ВНЕШНЕГО C-ИНТЕРФЕЙСА (экспортируемые функции)
// ==============================================================================================

extern "C" {

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ РАБОТЫ СО ШРИФТАМИ
    // ==========================================================================================

    /**
     * @brief Загружает шрифт из файла
     * @param path Путь к файлу шрифта
     * @return Указатель на загруженный шрифт или nullptr в случае ошибки
     */
    MOON_API FontPtr loadSystemFont(const char* path) {
        FontPtr font = new sf::Font();
        try {
            // Попытка загрузки шрифта из файла
            if (!font->loadFromFile(path)) {
                delete font;  // Важно: освобождаем память при неудачной загрузке
                return nullptr;
            }
        } catch (const std::exception& e) {
            delete font;  // Освобождаем память в случае исключения
            return nullptr;
        }
        // Отключаем сглаживание для более четкого отображения
        font->setSmooth(false);
        return font;
    }

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ СОЗДАНИЯ И УПРАВЛЕНИЯ ТЕКСТОМ
    // ==========================================================================================

    /**
     * @brief Создает объект текста с указанным шрифтом
     * @param font Указатель на шрифт
     * @return Указатель на созданный объект текста
     */
    MOON_API TextPtr createText(FontPtr font) {
        TextPtr text = new sf::Text();
        text->setFont(*font);
        return text;
    }

    /**
     * @brief Устанавливает текстовое содержимое
     * @param text Указатель на объект текста
     * @param str Строка для отображения (в кодировке UTF-8)
     */
    MOON_API void setText(TextPtr text, const char* str) {
        std::string std_str(str);
        // Преобразование из UTF-8 в внутренний формат SFML
        text->setString(sf::String::fromUtf8(std_str.begin(), std_str.end()));
    }

    /**
     * @brief Устанавливает размер символов текста
     * @param text Указатель на объект текста
     * @param size Размер шрифта в пикселях
     */
    MOON_API void setTextSize(TextPtr text, int size) {
        text->setCharacterSize(size);
    }

    /**
     * @brief Устанавливает масштаб текста
     * @param text Указатель на объект текста
     * @param scaleX Масштаб по оси X
     * @param scaleY Масштаб по оси Y
     */
    MOON_API void setTextScale(TextPtr text, float scaleX, float scaleY) {
        text->setScale(scaleX, scaleY);
    }

    /**
     * @brief Устанавливает цвет текста
     * @param text Указатель на объект текста
     * @param r Красная компонента цвета (0-255)
     * @param g Зеленая компонента цвета (0-255)
     * @param b Синяя компонента цвета (0-255)
     * @param a Альфа-компонента (прозрачность, 0-255)
     */
    MOON_API void setTextColor(TextPtr text, int r, int g, int b, int a) {
        text->setFillColor(sf::Color(r, g, b, a));
    }

    /**
     * @brief Устанавливает позицию текста на экране
     * @param text Указатель на объект текста
     * @param x Координата X
     * @param y Координата Y
     */
    MOON_API void setTextPosition(TextPtr text, float x, float y) {
        text->setPosition(x, y);
    }

    /**
     * @brief Устанавливает точку отсчета (origin) для трансформаций текста
     * @param text Указатель на объект текста
     * @param x Смещение по X относительно левого верхнего угла
     * @param y Смещение по Y относительно левого верхнего угла
     */
    MOON_API void setTextOffset(TextPtr text, float x, float y) {
        text->setOrigin(x, y);
    }

    /**
     * @brief Устанавливает угол поворота текста
     * @param text Указатель на объект текста
     * @param angle Угол поворота в градусах
     */
    MOON_API void setTextAngle(TextPtr text, float angle) {
        text->setRotation(angle);
    }

    /**
     * @brief Устанавливает стиль текста (жирный, курсив, подчеркнутый)
     * @param text Указатель на объект текста
     * @param style Комбинация флагов стиля из sf::Text::Style
     */
    MOON_API void setStyle(TextPtr text, sf::Text::Style style) {
        text->setStyle(style);
    }

    /**
     * @brief Устанавливает цвет контура текста
     * @param text Указатель на объект текста
     * @param r Красная компонента цвета (0-255)
     * @param g Зеленая компонента цвета (0-255)
     * @param b Синяя компонента цвета (0-255)
     * @param a Альфа-компонента (прозрачность, 0-255)
     */
    MOON_API void setOutlineColor(TextPtr text, int r, int g, int b, int a) {
        text->setOutlineColor(sf::Color(r, g, b, a));
    }

    /**
     * @brief Устанавливает толщину контура текста
     * @param text Указатель на объект текста
     * @param thickness Толщина контура в пикселях
     */
    MOON_API void setOutlineThickness(TextPtr text, float thickness) {
        text->setOutlineThickness(thickness);
    }

    /**
     * @brief Устанавливает межбуквенное расстояние
     * @param text Указатель на объект текста
     * @param spacing Коэффициент межбуквенного расстояния
     */
    MOON_API void setLetterSpacing(TextPtr text, float spacing) {
        text->setLetterSpacing(spacing);
    }

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ ИНФОРМАЦИИ О ТЕКСТЕ
    // ==========================================================================================

    /**
     * @brief Возвращает ширину текста в пикселях
     * @param text Указатель на объект текста
     * @return Ширина текста с учетом всех трансформаций
     */
    MOON_API double getTextWidth(TextPtr text) {
        return text->getGlobalBounds().width;
    }

    /**
     * @brief Возвращает высоту текста в пикселях
     * @param text Указатель на объект текста
     * @return Высота текста с учетом всех трансформаций
     */
    MOON_API double getTextHeight(TextPtr text) {
        return text->getGlobalBounds().height;
    }

    // ==========================================================================================
    // ФУНКЦИИ ДЛЯ ИЗМЕНЕНИЯ СВОЙСТВ ТЕКСТА
    // ==========================================================================================

    /**
     * @brief Изменяет шрифт для текста
     * @param text Указатель на объект текста
     * @param font Указатель на новый шрифт
     */
    MOON_API void setFont(TextPtr text, FontPtr font) {
        text->setFont(*font);
    }

} // extern "C"

// ==============================================================================================
// КОНЕЦ ФАЙЛА
// ==============================================================================================
// ================================================================================
//                         BUILDED_GRAPHICS.cpp
//                    Биндинги для работы с графикой в PySGL
// ================================================================================
//
// Этот файл содержит C++ функции для работы с графическими компонентами SFML,
// которые экспортируются в Python через ctypes.
//
// Основные компоненты:
// - Работа с RenderTexture (оффскринный рендеринг)
// - Управление текстурами (загрузка, настройки, подтекстуры)
// - Операции со спрайтами (трансформации, свойства, отрисовка)
// - Настройки рендеринга и состояний отрисовки
//
// ================================================================================
#include "SFML/Graphics/Image.hpp"
#include "SFML/Graphics/RenderTexture.hpp"
#include "SFML/Graphics/RenderTarget.hpp"
#include "SFML/Graphics/RenderStates.hpp"
#include "SFML/Graphics/Drawable.hpp"
#include "SFML/Graphics/Texture.hpp"
#include "SFML/Graphics/Shader.hpp"
#include "SFML/Graphics/Sprite.hpp"
#include "SFML/Graphics/Color.hpp"
#include "SFML/Graphics/Rect.hpp"
#include "SFML/Graphics/View.hpp"

#include "SFML/Window/ContextSettings.hpp"




#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

// ================================================================================
//                         RENDER TEXTURE (ОФФСКРИННЫЙ РЕНДЕРИНГ)
// ================================================================================
// Функции для работы с RenderTexture - текстурой, в которую можно отрисовывать
// ================================================================================

extern "C" {

    typedef sf::RenderTexture* RenderTexturePtr;
    typedef sf::Texture* TexturePtr;
    typedef sf::View* ViewPtr;
    typedef sf::Sprite* SpritePtr;
    typedef sf::Image* ImagePtr;


    // Создание нового объекта RenderTexture
    MOON_API RenderTexturePtr
    _RenderTexture_Init() {
        return new sf::RenderTexture();
    }

    // Инициализация RenderTexture с указанными размерами
    MOON_API bool
    _RenderTexture_Create(RenderTexturePtr texture, int width, int height) {
        return texture->create(width, height);
    }

    MOON_API bool
    _RenderTexture_CreateWithContextSettings(RenderTexturePtr texture, int width, int height, sf::ContextSettings settings) {
        return texture->create(width, height, settings);
    }

    // Отрисовка Drawable объекта в RenderTexture
    MOON_API void
    _RenderTexture_Draw(RenderTexturePtr texture, sf::Drawable* shape) {
        texture->draw(*shape);
    }

    // Отрисовка объекта с применением шейдера
    MOON_API void
    _RenderTexture_DrawWithShader(RenderTexturePtr texture, sf::Drawable* shape, sf::Shader* shader) {
        texture->draw(*shape, shader);
    }

    // Отрисовка объекта с кастомными RenderStates
    MOON_API void
    _RenderTexture_DrawWithRenderStates(RenderTexturePtr texture, sf::Drawable* shape, sf::RenderStates* render_states) {
        texture->draw(*shape, *render_states);
    }

    // Очистка RenderTexture указанным цветом
    MOON_API void
    _RenderTexture_Clear(RenderTexturePtr texture, int r, int g, int b, int a) {
        texture->clear(sf::Color(r, g, b, a));
    }

    // Обновление текстуры после отрисовки (финализация кадра)
    MOON_API void
    _RenderTexture_Display(RenderTexturePtr texture) {
        texture->display();
    }

    // Включение/выключение сглаживания для текстуры
    MOON_API void
    _RenderTexture_SetSmooth(RenderTexturePtr texture, bool smooth) {
        texture->setSmooth(smooth);
    }

    // Установка камеры (вида) для RenderTexture
    MOON_API void
    _RenderTexture_SetView(RenderTexturePtr texture, ViewPtr view) {
        texture->setView(*view);
    }

    // Получение дефолтного вида RenderTexture
    MOON_API ViewPtr
    _RenderTexture_GetDefaultView(RenderTexturePtr texture) {
        return new sf::View(texture->getDefaultView());
    }

    // Получение текущего установленного вида
    MOON_API ViewPtr
    _RenderTexture_GetView(RenderTexturePtr texture) {
        return new sf::View(texture->getView());
    }

    // Получение текстуры из RenderTexture для использования
    // Возвращает указатель на новую текстуру созданную из RenderTexture
    MOON_API TexturePtr
    _RenderTexture_GetTexture(RenderTexturePtr texture) {
        return new sf::Texture(texture->getTexture());
    }

    // Удаление объекта RenderTexture и освобождение памяти
    MOON_API void
    _RenderTexture_Delete(RenderTexturePtr texture) {
        delete texture;
    }
}

// ================================================================================
//                               ТЕКСТУРЫ
// ================================================================================
// Функции для загрузки, управления и манипуляций с текстурами
// ================================================================================

extern "C" {
    // Инициализация текстуры
    MOON_API TexturePtr _Texture_Init() {
        TexturePtr texture = new sf::Texture();
        return texture;
    }

    // Загрузка текстуры из файла
    // Возвращает true, если загрузка прошла успешно, иначе false
    MOON_API bool _Texture_LoadFromFile(TexturePtr texture,  char* file_path) {
        bool result = texture->loadFromFile(file_path);
        return result;
    }

    // Загрузка текстуры из файла с указанием области загрузки
    // Возвращает true, если загрузка прошла успешно, иначе false
    MOON_API bool _Texture_LoadFromFileWithBoundRect(TexturePtr texture, char* file_path, int x, int y, int w, int h) {
        bool result = texture->loadFromFile(file_path, sf::IntRect(x, y ,w, h));
        return result;
    }

    // Удаление текстуры и освобождение памяти
    MOON_API void _Texture_Delete(TexturePtr texture) {
        delete texture;
    }

    // Получение максимального поддерживаемого размера текстуры
    MOON_API int _Texture_GetMaximumSize(TexturePtr texture) {
        return texture->getMaximumSize();
    }

    // Получение ширины текстуры
    MOON_API int _Texture_GetSizeX(TexturePtr texture) {
        return texture->getSize().x;
    }

    // Получение высоты текстуры
    MOON_API int _Texture_GetSizeY(TexturePtr texture) {
        return texture->getSize().y;
    }

    // Включение/выключение режима повторения текстуры
    MOON_API void _Texture_SetRepeated(TexturePtr texture, bool value) {
        texture->setRepeated(value);
    }

    // Включение/выключение сглаживания текстуры
    MOON_API void _Texture_SetSmooth(TexturePtr texture, bool value) {
        texture->setSmooth(value);
    }

    // Обмен данными между двумя текстурами
    MOON_API void _Texture_Swap(TexturePtr texture, TexturePtr texture2) {
        texture->swap(*texture2);
    }

    // Создание текстуры из области существующей текстуры
    MOON_API TexturePtr _Texture_SubTexture(TexturePtr texture, int x, int y, int w, int h) {
        // Создаем спрайт для отрисовки части текстуры
        sf::Sprite sprite(*texture, sf::IntRect(x, y, w, h));
        
        // Создаем целевой render texture
        sf::RenderTexture renderTexture;
        if (!renderTexture.create(w, h)) {
            // Если не удалось создать render texture, возвращаем nullptr
            return nullptr;
        }
        
        // Очищаем прозрачным цветом и рисуем нужную область
        renderTexture.clear(sf::Color::Transparent);
        renderTexture.draw(sprite);
        renderTexture.display();
        
        // Создаем новую текстуру из render texture
        TexturePtr subTexture = new sf::Texture(renderTexture.getTexture());
        
        return subTexture;
    }
}

// ================================================================================
//                               СПРАЙТЫ
// ================================================================================
// Функции для создания, трансформации и управления спрайтами
// ================================================================================

extern "C" {

    
    // Создает новый спрайт
    MOON_API SpritePtr _Sprite_Init() {
        return new sf::Sprite();
    }

    // Удаляет спрайт
    // Очищает память, выделенную для спрайта
    MOON_API void _Sprite_Delete(SpritePtr sprite) {
        delete sprite;
    }

    // Устанавливает текстуру для спрайта
    // Сохраняет ссылку на текстуру для спрайта
    // При удалении спрайта, текстура не будет удалена
    // При удалении текстуры, поведение не определено
    MOON_API void _Sprite_LinkTexture(SpritePtr sprite, TexturePtr texture, bool reset_rect = true) {
        sprite->setTexture(*texture, reset_rect);
    }

    // Устанавливает текстуру для спрайта
    // Сохраняет ссылку на текстуру для спрайта
    // При удалении спрайта, текстура не будет удалена
    // При удалении текстуры, поведение не определено
    MOON_API void _Sprite_LinkRenderTexture(SpritePtr sprite, RenderTexturePtr texture, bool reset_rect = true) {
        sprite->setTexture(texture->getTexture(), reset_rect);
    }

    // Устанавливает область на текстуре которая будет отображаться на спрайте
    MOON_API void _Sprite_SetTextureRect(SpritePtr sprite, const int x, const int y, const int width, const int height) {
        sprite->setTextureRect(sf::IntRect(x, y, width, height));
    }

    // Устанавливает масштаб спрайта
    MOON_API void _Sprite_SetScale(SpritePtr sprite, double scale_x, double scale_y) {
        sprite->setScale(scale_x, scale_y);
    }

    // Устанавливает поворот спрайта
    MOON_API void _Sprite_SetRotation(SpritePtr sprite, double angle) {
        sprite->setRotation(angle);
    }

    // Устанавливает позицию спрайта
    MOON_API void _Sprite_SetPosition(SpritePtr sprite, double x, double y) {
        sprite->setPosition(x, y);
    }

    // Устанавливает ориентацию спрайта
    MOON_API void _Sprite_SetOrigin(SpritePtr sprite, double x, double y) {
        sprite->setOrigin(x, y);
    }

    MOON_API void _Sprite_SetColor(SpritePtr sprite, const int r, const int g, const int b, const int a) {
        sprite->setColor(sf::Color(r, g, b, a));
    }

    // Функции для получения цвета спрайта
    /////////////////////////////////////////////////////////////////////////////////
    MOON_API int _Sprite_GetColorR(SpritePtr sprite) {
        return sprite->getColor().r;
    }

    MOON_API int _Sprite_GetColorG(SpritePtr sprite) {
        return sprite->getColor().g;
    }

    MOON_API int _Sprite_GetColorB(SpritePtr sprite) {
        return sprite->getColor().b;
    }

    MOON_API int _Sprite_GetColorA(SpritePtr sprite) {
        return sprite->getColor().a;
    }
    /////////////////////////////////////////////////////////////////////////////////

    // Получение угла поворота спрайта
    MOON_API int _Sprite_GetRotation(SpritePtr sprite) {
        return sprite->getRotation();
    }

    // Функции для получения масштаба спрайта
    /////////////////////////////////////////////////////////////////////////////////
    MOON_API double _Sprite_GetScaleX(SpritePtr sprite) {
        return sprite->getScale().x;
    }

    MOON_API double _Sprite_GetScaleY(SpritePtr sprite) {
        return sprite->getScale().y;
    }
    /////////////////////////////////////////////////////////////////////////////////

    MOON_API double _Sprite_GetPositionX(SpritePtr sprite) {
        return sprite->getPosition().x;
    }

    MOON_API double _Sprite_GetPositionY(SpritePtr sprite) {
        return sprite->getPosition().y;
    }

    MOON_API double _Sprite_GetGlobalBoundRectX(SpritePtr sprite) {
        return sprite->getGlobalBounds().left;
    }

    MOON_API double _Sprite_GetGlobalBoundRectY(SpritePtr sprite) {
        return sprite->getGlobalBounds().top;
    }

    MOON_API double _Sprite_GetGlobalBoundRectW(SpritePtr sprite) {
        return sprite->getGlobalBounds().width;
    }

    MOON_API double _Sprite_GetGlobalBoundRectH(SpritePtr sprite) {
        return sprite->getGlobalBounds().height;
    }

    MOON_API void _Sprite_Rotate(SpritePtr sprite, double angle) {
        sprite->rotate(angle);
    }

    MOON_API void _Sprite_Scale(SpritePtr sprite, double scale_x, double scale_y) {
        sprite->scale(scale_x, scale_y);
    }

    // напиши метод для получения локальных границ содержимого спрайта
    MOON_API double _Sprite_GetLocalBoundRectX(SpritePtr sprite) {
        return sprite->getLocalBounds().left;
    }

    MOON_API double _Sprite_GetLocalBoundRectY(SpritePtr sprite) {
        return sprite->getLocalBounds().top;
    }

    MOON_API double _Sprite_GetLocalBoundRectW(SpritePtr sprite) {
        return sprite->getLocalBounds().width;
    }

    MOON_API double _Sprite_GetLocalBoundRectH(SpritePtr sprite) {
        return sprite->getLocalBounds().height;
    }
}

extern "C" {
    MOON_API ImagePtr _Image_Init() {
        return new sf::Image();
    }

    MOON_API ImagePtr _Image_TextureCopyToImage(TexturePtr texture) {
        return new sf::Image(texture->copyToImage());
    }

    MOON_API ImagePtr _Image_RenderTextureCopyToImage(RenderTexturePtr texture) {
        return new sf::Image(texture->getTexture().copyToImage());
    }

    MOON_API void _Image_Delete(ImagePtr image) {
        delete image;
    }

    MOON_API bool _Image_Save(ImagePtr image, char* file_name) {
        return image->saveToFile(file_name);
    }
}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с графикой PySGL определены.
// Они предоставляют полный интерфейс для работы с текстурами,
// RenderTexture и спрайтами в Python приложениях.
// ================================================================================

#include "SFML/Graphics/Color.hpp"
#include "SFML/Graphics/PrimitiveType.hpp"
#include "SFML/Graphics/VertexArray.hpp"
#include "SFML/Graphics/Vertex.hpp"
#include "SFML/System/Vector2.hpp"
#include <cstddef>


#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::VertexArray* VertexArrayPtr;
typedef sf::Vertex* VertexPtr;

extern "C" {
    MOON_API VertexPtr _Vertex_Init() {
        return new sf::Vertex();
    }

    MOON_API VertexPtr _Vertex_InitFromCoords(double x, double y) {
        return new sf::Vertex(sf::Vector2f(x, y));
    }

    MOON_API VertexPtr _Vertex_InitFromCoordsAndColor(double x, double y, int r, int g, int b, int a) {
        return new sf::Vertex(sf::Vector2f(x, y), sf::Color(r, g, b, a));
    }

    MOON_API VertexPtr _Vertex_InitFromCoordsAndColorAndTexCoords(double x, double y, int r, int g, int b, int a, int tx, int ty) {
        return new sf::Vertex(sf::Vector2f(x, y), sf::Color(r, g, b, a), sf::Vector2f(tx, ty));
    }

    MOON_API void _Vertex_Delete(VertexPtr vertex) {
        delete vertex;
    }

    MOON_API void _Vertex_SetPosition(VertexPtr vertex, double x, double y) {
        vertex->position = sf::Vector2f(x, y);
    }

    MOON_API void _Vertex_SetColor(VertexPtr vertex, int r, int g, int b, int a) {
        vertex->color = sf::Color(r, g, b, a);
    }

    MOON_API void _Vertex_SetTexCoords(VertexPtr vertex, double tx, double ty) {
        vertex->texCoords = sf::Vector2f(tx, ty);
    }

    MOON_API double _Vertex_GetPositionX(VertexPtr vertex) {
        return vertex->position.x;
    }

    MOON_API double _Vertex_GetPositionY(VertexPtr vertex) {
        return vertex->position.y;
    }

    MOON_API double _Vertex_GetTexCoordX(VertexPtr vertex) {
        return vertex->texCoords.x;
    }

    MOON_API double _Vertex_GetTexCoordY(VertexPtr vertex) {
        return vertex->texCoords.y;
    }

    MOON_API int _Vertex_GetColorR(VertexPtr vertex) {
        return vertex->color.r;
    }

    MOON_API int _Vertex_GetColorG(VertexPtr vertex) {
        return vertex->color.g;
    }

    MOON_API int _Vertex_GetColorB(VertexPtr vertex) {
        return vertex->color.b;
    }

    MOON_API int _Vertex_GetColorA(VertexPtr vertex) {
        return vertex->color.a;
    }
}

extern "C" {
    MOON_API VertexArrayPtr _VertexArray_Init() {
        return new sf::VertexArray();
    }

    MOON_API void _VertexArray_Delete(VertexArrayPtr array) {
        delete array;
    }

    MOON_API void _VertexArray_SetPrimitiveType(VertexArrayPtr array, int type) {
        array->setPrimitiveType(static_cast<sf::PrimitiveType>(type));
    }

    MOON_API void _VertexArray_Clear(VertexArrayPtr array) {
        array->clear();
    }

    MOON_API int _VertexArray_GetVertexCount(VertexArrayPtr array) {
        return array->getVertexCount();
    }

    MOON_API double _VertexArray_GetBoundsPosX(VertexArrayPtr array) {
        return array->getBounds().left;
    }

    MOON_API double _VertexArray_GetBoundsPosY(VertexArrayPtr array) {
        return array->getBounds().top;
    }

    MOON_API double _VertexArray_GetBoundsSizeW(VertexArrayPtr array) {
        return array->getBounds().width;
    }

    MOON_API double _VertexArray_GetBoundsSizeH(VertexArrayPtr array) {
        return array->getBounds().height;
    }

    MOON_API void _VertexArray_Resize(VertexArrayPtr array, int count) {
        array->resize(count);
    }

    MOON_API bool _VertexArray_IsEmpty(VertexArrayPtr array) {
        return array->getVertexCount() == 0;
    }

    MOON_API void _VertexArray_AppendVertex(VertexArrayPtr array, VertexPtr vertex) {
        array->append(*vertex);
    }

    MOON_API VertexPtr _VertexArray_GetVertex(VertexArrayPtr array, int index) {
        return &(*array)[index];
    }

    MOON_API void _VertexArray_RemoveVertex(VertexArrayPtr array, int index) {
        int vertexCount = array->getVertexCount();
        if (index < 0 || index >= vertexCount) return;

        // Сдвигаем все вершины после удаляемой
        for (int i = index; i < vertexCount - 1; ++i) {
            (*array)[i] = (*array)[i + 1];
        }

        // Уменьшаем размер на 1
        array->resize(vertexCount - 1);
    }

    MOON_API void _VertexArray_InsertVertex(VertexArrayPtr array, int index, VertexPtr vertex) {
            int vertexCount = array->getVertexCount();
            if (index < 0 || index > vertexCount) return; // index == vertexCount означает добавление в конец

            // Увеличиваем размер массива
            array->resize(vertexCount + 1);

            // Сдвигаем вершины от конца до позиции вставки
            for (int i = vertexCount; i > index; --i) {
                (*array)[i] = (*array)[i - 1];
            }

            // Вставляем новую вершину
            (*array)[index] = *vertex;
        }

    MOON_API void _VertexArray_PrependVertex(VertexArrayPtr array, VertexPtr vertex) {
        // Просто вызываем insert с индексом 0
        _VertexArray_InsertVertex(array, 0, vertex);
    }

    MOON_API void _VertexArray_SetColor(VertexArrayPtr array, int r, int g, int b, int a) {
        int vertexCount = array->getVertexCount();
        for (int i = 0; i < vertexCount; ++i) {
            (*array)[i].color = sf::Color(r, g, b, a);
        }
    }
}

// ================================================================================
//                           BUILDED_SGL_VIEW.cpp
//                    Биндинги для работы с видами и прямоугольниками
// ================================================================================
//
// Этот файл содержит C++ функции для работы с прямоугольниками и видами (View) SFML,
// которые экспортируются в Python через ctypes.
//
// Основные компоненты:
// - Создание и управление прямоугольниками (FloatRect)
// - Работа с видами (View) - камерами и областями просмотра
// - Преобразования координат и геометрические операции
// - Управление размерами, позициями и углами поворота
//
// ================================================================================

#ifndef SFML_GRAPHICS_HPP
#include <SFML/Graphics/Rect.hpp>
#include <SFML/Graphics/View.hpp>
#endif

typedef sf::View* ViewPtr;
typedef sf::FloatRect* FloatRectPtr;

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

// ================================================================================
//                           РАБОТА С ПРЯМОУГОЛЬНИКАМИ
// ================================================================================
// Функции для создания и управления прямоугольными областями:
// - Создание прямоугольников с заданными параметрами
// - Получение и установка позиции и размера
// - Геометрические операции
// ================================================================================

extern "C" {

    // Создание нового прямоугольника с указанными параметрами
    MOON_API FloatRectPtr _FloatRect_Create(float rect_left, float rect_top, float rect_width, float rect_height) {
        return new sf::FloatRect(rect_left, rect_top, rect_width, rect_height);
    }

    // Удаление прямоугольника и освобождение памяти
    MOON_API void _FloatRect_Delete(FloatRectPtr rect) {
        delete rect;
    }

    // ================================================================================
    //                   ПОЛУЧЕНИЕ СВОЙСТВ ПРЯМОУГОЛЬНИКА
    // ================================================================================

    // Получение X-координаты позиции прямоугольника
    MOON_API float _FloatRect_GetPositionX(FloatRectPtr rect) {
        return rect->getPosition().x;
    }

    // Получение Y-координаты позиции прямоугольника
    MOON_API float _FloatRect_GetPositionY(FloatRectPtr rect) {
        return rect->getPosition().y;
    }

    // Получение ширины прямоугольника
    MOON_API float _FloatRect_GetWidth(FloatRectPtr rect) {
        return rect->getSize().x;
    }

    // Получение высоты прямоугольника
    MOON_API float _FloatRect_GetHeight(FloatRectPtr rect) {
        return rect->getSize().y;
    }

    // ================================================================================
    //                   УСТАНОВКА СВОЙСТВ ПРЯМОУГОЛЬНИКА
    // ================================================================================

    // Установка позиции прямоугольника
    MOON_API void _FloatRect_SetPosition(FloatRectPtr rect, float x, float y) {
        rect->left = x;
        rect->top = y;
    }

    // Установка размера прямоугольника
    MOON_API void _FloatRect_SetSize(FloatRectPtr rect, float w, float h) {
        rect->width = w;
        rect->height = h;
    }
}

// ================================================================================
//                           РАБОТА С ВИДАМИ (VIEW)
// ================================================================================
// Функции для создания и управления видами (камерами):
// - Создание видов на основе прямоугольников
// - Управление центром, размером и поворотом
// - Операции перемещения, масштабирования и вращения
// - Настройка области просмотра (viewport)
// ================================================================================

extern "C" {

    // Создание нового вида на основе прямоугольника
    MOON_API ViewPtr _View_Create(FloatRectPtr rect) {
        ViewPtr view = new sf::View(*rect);
        return view;
    }

    // Удаление вида и освобождение памяти
    MOON_API void _View_Delete(ViewPtr view) {
        delete view;
    }

    // ================================================================================
    //                   ПОЛУЧЕНИЕ СВОЙСТВ ВИДА
    // ================================================================================

    // Получение X-координаты позиции области просмотра
    MOON_API float _View_GetPositionX(ViewPtr view) {
        return view->getViewport().left;
    }

    // Получение Y-координаты позиции области просмотра
    MOON_API float _View_GetPositionY(ViewPtr view) {
        return view->getViewport().top;
    }

    // Получение X-координаты центра вида
    MOON_API float _View_GetCenterX(ViewPtr view) {
        return view->getCenter().x;
    }

    // Получение Y-координаты центра вида
    MOON_API float _View_GetCenterY(ViewPtr view) {
        return view->getCenter().y;
    }

    // Получение угла поворота вида в градусах
    MOON_API float _View_GetAngle(ViewPtr view) {
        return view->getRotation();
    }

    // Получение ширины вида
    MOON_API float _View_GetWidth(ViewPtr view) {
        return view->getSize().x;
    }

    // Получение высоты вида
    MOON_API float _View_GetHeight(ViewPtr view) {
        return view->getSize().y;
    }

    // ================================================================================
    //                   ПРЕОБРАЗОВАНИЯ И ОПЕРАЦИИ ВИДА
    // ================================================================================

    // Поворот вида на указанный угол (градусы)
    MOON_API void _View_Rotate(ViewPtr view, float angle) {
        view->rotate(angle);
    }

    // Перемещение вида на указанное смещение
    MOON_API void _View_Move(ViewPtr view, float x, float y) {
        view->move(x, y);
    }

    // Масштабирование вида (зум)
    MOON_API void _View_Zoom(ViewPtr view, float zoom) {
        view->zoom(zoom);
    }

    // ================================================================================
    //                   УСТАНОВКА СВОЙСТВ ВИДА
    // ================================================================================

    // Сброс вида к состоянию на основе прямоугольника
    MOON_API void _View_Reset(ViewPtr view, FloatRectPtr rect) {
        view->reset(*rect);
    }

    // Установка центра вида
    MOON_API void _View_SetCenter(ViewPtr view, float x, float y) {
        view->setCenter(x, y);
    }

    // Установка угла поворота вида (градусы)
    MOON_API void _View_SetAngle(ViewPtr view, float angle) {
        view->setRotation(angle);
    }

    // Установка области просмотра (нормализованные координаты)
    MOON_API void _View_SetViewport(ViewPtr view, FloatRectPtr rect) {
        view->setViewport(*rect);
    }

    // Установка размера вида
    MOON_API void _View_SetSize(ViewPtr view, float w, float h) {
        view->setSize(w, h);
    }
}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с прямоугольниками и видами PySGL определены.
// Они предоставляют полный интерфейс для управления камерами и
// геометрическими областями в Python приложениях.
// ================================================================================

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

// ================================================================================
//                         BUILDED_WINDOWEVENTS.cpp
//                    Биндинги для работы с событиями окон в PySGL
// ================================================================================
//
// Этот файл содержит C++ функции для работы с событиями SFML,
// которые экспортируются в Python через ctypes.
//
// Основные компоненты:
// - Создание и управление объектами событий
// - Получение информации о событиях клавиатуры
// - Обработка событий мыши (кнопки, координаты, колесо)
// - События изменения размера окна
// - Типизация и классификация событий
//
// ================================================================================

#ifndef SFML_WINDOW_HPP
#include <SFML/Window/Event.hpp>
#endif

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

// ================================================================================
//                        УПРАВЛЕНИЕ ОБЪЕКТАМИ СОБЫТИЙ
// ================================================================================
// Функции для создания, удаления и базовой работы с событиями:
// - Создание новых объектов событий
// - Освобождение памяти
// - Получение типа события
// ================================================================================

extern "C" {
    // Создание нового объекта события для хранения данных
    MOON_API sf::Event* _Events_Create() {
        return new sf::Event();
    }

    // Удаление объекта события и освобождение памяти
    MOON_API void _Events_Destroy(sf::Event* event) {
        delete event;
    }

    // Получение типа текущего события (Closed, KeyPressed, MouseMoved и т.д.)
    MOON_API int _Events_GetType(sf::Event* event) {
        return event->type;
    }

    // ================================================================================
    //                          СОБЫТИЯ КЛАВИАТУРЫ
    // ================================================================================
    // Функции для обработки событий клавиатуры

    // Получение кода нажатой/отпущенной клавиши
    MOON_API int _Events_GetKey(sf::Event* event) {
        return event->key.code;
    }

    // ================================================================================
    //                            СОБЫТИЯ МЫШИ
    // ================================================================================
    // Функции для обработки всех типов событий мыши

    // Получение кода нажатой кнопки мыши (0-левая, 1-правая, 2-средняя)
    MOON_API int _Events_GetMouseButton(sf::Event* event) {
        return event->mouseButton.button;
    }

    // Получение X-координаты курсора мыши в момент события
    MOON_API int _Events_GetMouseX(sf::Event* event) {
        return event->mouseButton.x;
    }

    // Получение Y-координаты курсора мыши в момент события
    MOON_API int _Events_GetMouseY(sf::Event* event) {
        return event->mouseButton.y;
    }

    // Получение значения прокрутки колеса мыши (положительное - вверх, отрицательное - вниз)
    MOON_API int _Events_GetMouseWheel(sf::Event* event) {
        return event->mouseWheel.delta;
    }

    // ================================================================================
    //                      СОБЫТИЯ ИЗМЕНЕНИЯ РАЗМЕРА ОКНА
    // ================================================================================
    // Функции для получения новых размеров окна при событии Resized

    // Получение новой ширины окна после изменения размера (в пикселях)
    MOON_API int _Events_GetSizeWidth(sf::Event* event) {
        return event->size.width;
    }

    // Получение новой высоты окна после изменения размера (в пикселях)
    MOON_API int _Events_GetSizeHeight(sf::Event* event) {
        return event->size.height;
    }
}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с событиями PySGL определены.
// Они предоставляют полный интерфейс для обработки пользовательского ввода
// и системных событий в Python приложениях.
// ================================================================================


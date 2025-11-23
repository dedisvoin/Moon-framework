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
#include "SFML/OpenGL.hpp"

#include <cstddef>
#include <gl/GL.h>
#include <variant>


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

    MOON_API const char* _Glsl_GetVersion() {
        static char version[128] = {0};
        const char* gl_version = (const char*)glGetString(GL_VERSION);
        
        if (gl_version) {
            strncpy(version, gl_version, sizeof(version) - 1);
            version[sizeof(version) - 1] = '\0';
        } else {
            strcpy(version, "noinit");
        }
        
        return version;
    }

    MOON_API const char* _Glsl_GetVendor() {
        static char version[128] = {0};
        const char* gl_version = (const char*)glGetString(GL_VENDOR);
        
        if (gl_version) {
            strncpy(version, gl_version, sizeof(version) - 1);
            version[sizeof(version) - 1] = '\0';
        } else {
            strcpy(version, "noinit");
        }
        
        return version;
    }

    MOON_API const char* _Glsl_GetRenderer() {
        static char version[128] = {0};
        const char* gl_version = (const char*)glGetString(GL_RENDERER);
        
        if (gl_version) {
            strncpy(version, gl_version, sizeof(version) - 1);
            version[sizeof(version) - 1] = '\0';
        } else {
            strcpy(version, "noinit");
        }
        
        return version;
    }

    // Создание нового объекта шейдера
    MOON_API ShaderPtr _Shader_Create() {
        
        return new sf::Shader();
    }

    MOON_API void _Shader_Delete(ShaderPtr shader) {
        delete shader;
    }

    MOON_API bool _Shader_IsAvailable() {
        return sf::Shader::isAvailable();
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

    // ================================================================================
    //                   НАСТРОЙКА УНИФОРМ (ПАРАМЕТРОВ ШЕЙДЕРОВ)
    // ================================================================================

    MOON_API void _Shader_SetUniformFloatArray(ShaderPtr shader, char* name, float* values, size_t count) {
        shader->setUniformArray(name, values, count);
    }

    // Установка целочисленной униформы
    MOON_API void _Shader_SetUniformInt(ShaderPtr shader, char* name, float value) {
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
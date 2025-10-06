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
#include "SFML/Graphics/RenderTexture.hpp"
#include "SFML/Graphics/RenderTarget.hpp"
#include "SFML/Graphics/RenderStates.hpp"
#include "SFML/Graphics/Drawable.hpp"
#include "SFML/Graphics/Shader.hpp"
#include "SFML/Graphics/Color.hpp"
#include "SFML/Graphics/Sprite.hpp"
#include "SFML/Graphics/Rect.hpp"
#include "SFML/Graphics/Texture.hpp"
#include "SFML/Graphics/View.hpp"
#include "SFML/Window/ContextSettings.hpp"
#include "SFML/OpenGL.hpp"



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
    MOON_API int _Texture_GetMaxixmumSize(TexturePtr texture) {
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
        // Создаем новую текстуру
        TexturePtr subTexture = new sf::Texture();

        // Активируем контекст исходной текстуры
        sf::Texture::bind(texture);

        // Создаем новую текстуру нужного размера
        subTexture->create(w, h);

        // Копируем область напрямую через OpenGL
        sf::Texture::bind(subTexture);
        glCopyTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, x, y, w, h);

        // Сбрасываем привязку текстур
        sf::Texture::bind(nullptr);
        return subTexture;
    }
}

// ================================================================================
//                               СПРАЙТЫ
// ================================================================================
// Функции для создания, трансформации и управления спрайтами
// ================================================================================

extern "C" {

    typedef sf::Sprite* SpritePtr;

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

    MOON_API void _Sprite(SpritePtr sprite, const int r, const int g, const int b, const int a) {
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
}

// ================================================================================
//                              КОНЕЦ ФАЙЛА
// ================================================================================
// Все функции для работы с графикой PySGL определены.
// Они предоставляют полный интерфейс для работы с текстурами,
// RenderTexture и спрайтами в Python приложениях.
// ================================================================================

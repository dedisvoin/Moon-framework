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
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

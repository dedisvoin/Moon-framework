#ifndef SFML_GRAPHICS_HPP
#include "SFML/Graphics/Rect.hpp"
#include "SFML/Graphics/View.hpp"
#endif

typedef sf::View* ViewPtr;
typedef sf::FloatRect* FloatRectPtr;

#define MOON_API __declspec(dllexport)

extern "C" {


    MOON_API FloatRectPtr _FloatRect_Create(float rect_left, float rect_top, float rect_width, float rect_height) {
        return new sf::FloatRect(rect_left, rect_top, rect_width, rect_height);
    }

    MOON_API void _FloatRect_Delete(FloatRectPtr rect) {
        delete rect;
    }

    MOON_API float _FloatRect_GetPositionX(FloatRectPtr rect) {
        return rect->getPosition().x;
    }

    MOON_API float _FloatRect_GetPositionY(FloatRectPtr rect) {
        return rect->getPosition().y;
    }

    MOON_API float _FloatRect_GetWidth(FloatRectPtr rect) {
        return rect->getSize().x;
    }

    MOON_API float _FloatRect_GetHeight(FloatRectPtr rect) {
        return rect->getSize().y;
    }

    MOON_API void _FloatRect_SetPosition(FloatRectPtr rect, float x, float y) {
        rect->left = x;
        rect->top = y;
    }

    MOON_API void _FloatRect_SetSize(FloatRectPtr rect, float w, float h) {
        rect->width = w;
        rect->height = h;
    }
}

extern "C" {
    MOON_API ViewPtr _View_Create(FloatRectPtr rect) {
        ViewPtr view = new sf::View(*rect);
        return view;
    }

    MOON_API void _View_Delete(ViewPtr view) {
        delete view;
    }

    MOON_API float _View_GetPositionX(ViewPtr view) {
        return view->getViewport().left;
    }

    MOON_API float _View_GetPositionY(ViewPtr view) {
        return view->getViewport().top;
    }

    MOON_API float _View_GetCenterX(ViewPtr view) {
        return view->getCenter().x;
    }

    MOON_API float _View_GetCenterY(ViewPtr view) {
        return view->getCenter().y;
    }

    MOON_API  float _View_GetAngle(ViewPtr view) {
        return view->getRotation();
    }

    MOON_API float _View_GetWidth(ViewPtr view) {
        return view->getSize().x;
    }

    MOON_API float _View_GetHeight(ViewPtr view) {
        return view->getSize().y;
    }

    MOON_API void _View_Rotate(ViewPtr view, float angle) {
        view->rotate(angle);
    }

    MOON_API void _View_Reset(ViewPtr view, FloatRectPtr rect) {
        view->reset(*rect);
    }

    MOON_API void _View_Move(ViewPtr view, float x, float y) {
        view->move(x, y);
    }

    MOON_API void _View_SetCenter(ViewPtr view, float x, float y) {
        view->setCenter(x, y);
    }

    MOON_API void _View_SetAngle(ViewPtr view, float angle) {
        view->setRotation(angle);
    }

    MOON_API void _View_SetViewport(ViewPtr view, FloatRectPtr rect) {
        view->setViewport(*rect);
    }

    MOON_API void _View_SetSize(ViewPtr view, float w, float h) {
        view->setSize(w, h);
    }

    MOON_API void _View_Zoom(ViewPtr view, float zoom) {
        view->zoom(zoom);
    }
}

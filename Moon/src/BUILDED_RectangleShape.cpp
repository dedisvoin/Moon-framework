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

    MOON_API double _Rectangle_GetOriginX(RectanglePtr rectangle) {
        return rectangle->getOrigin().x;
    }

    MOON_API double _Rectangle_GetOriginY(RectanglePtr rectangle) {
        return rectangle->getOrigin().y;
    }
}
// ===============================================================================
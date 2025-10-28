#include "SFML/Graphics/Color.hpp"
#include "SFML/Graphics/VertexArray.hpp"
#include "SFML/Graphics/Vertex.hpp"
#include "SFML/System/Vector2.hpp"


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
    
}

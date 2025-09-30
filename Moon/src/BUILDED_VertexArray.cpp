#include "SFML/Graphics/VertexArray.hpp"
#include "SFML/Graphics/Vertex.hpp"
#include "SFML/System/Vector2.hpp"

#include "SFML/Graphics/PrimitiveType.hpp"
#include <SFML/Graphics/RenderWindow.hpp>


#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

extern "C" {

    typedef sf::VertexArray* VertexArrayPtr;

    MOON_API VertexArrayPtr 
    _VertexArray_Create() {
        return new sf::VertexArray();
    }

    MOON_API void 
    _VertexArray_Delete(VertexArrayPtr vertexArray) {
        delete vertexArray;
    }

    MOON_API void 
    _VertexArray_AddVertexForPositionAndColor(VertexArrayPtr vertexArray, double x, double y, int r, int g, int b, int a) {
        vertexArray->append(sf::Vertex(sf::Vector2f(static_cast<float>(x), static_cast<float>(y)), sf::Color(static_cast<sf::Uint8>(r), static_cast<sf::Uint8>(g), static_cast<sf::Uint8>(b), static_cast<sf::Uint8>(a))));
    }

    MOON_API void 
    _VertexArray_SetPrimitiveType(VertexArrayPtr vertexArray, int primitiveType) {
        vertexArray->setPrimitiveType(static_cast<sf::PrimitiveType>(primitiveType));
    }

    MOON_API void 
    _VertexArray_Resize(VertexArrayPtr vertexArray, int vertexCount) {
        vertexArray->resize(static_cast<size_t>(vertexCount));
    }

    MOON_API void 
    _VertexArray_Clear(VertexArrayPtr vertexArray) {
        vertexArray->clear();
    }

    MOON_API int
    _VertexArray_GetVertexCount(VertexArrayPtr vertexArray) {
        return static_cast<int>(vertexArray->getVertexCount());
    }

    MOON_API float
    _VertexArray_GetVertexPositionX(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0.0f; 
        return vertexArray->operator[](index).position.x;
    }

    MOON_API float
    _VertexArray_GetVertexPositionY(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0.0f; 
        return vertexArray->operator[](index).position.y;
    }
        
    MOON_API int
    _VertexArray_GetVertexColorR(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.r;
    }
    
    MOON_API int
    _VertexArray_GetVertexColorG(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.g;
    }

    MOON_API int
    _VertexArray_GetVertexColorB(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0;
        return vertexArray->operator[](index).color.b;
    }
        
    MOON_API int
    _VertexArray_GetVertexColorA(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.a;
    }


    MOON_API void
    _VertexArray_SetVertexForPositionAndColor(VertexArrayPtr vertexArray, int index, double x, double y, int r, int g, int b, int a) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return; 
        vertexArray->operator[](index) = sf::Vertex(sf::Vector2f(static_cast<float>(x), static_cast<float>(y)), sf::Color(static_cast<sf::Uint8>(r), static_cast<sf::Uint8>(g), static_cast<sf::Uint8>(b), static_cast<sf::Uint8>(a)));
    }

    MOON_API int 
    _VertexArray_GetPrimitiveType(VertexArrayPtr vertexArray) {
        return static_cast<int>(vertexArray->getPrimitiveType());
    }

    // Оптимизированные функции для прямого доступа
    MOON_API void
    _VertexArray_SetVertexPosition(VertexArrayPtr vertexArray, int index, float x, float y) {
        if (index >= 0 && index < vertexArray->getVertexCount()) {
            (*vertexArray)[index].position = sf::Vector2f(x, y);
        }
    }


    MOON_API void
    _VertexArray_SetVertexColor(VertexArrayPtr vertexArray, int index, int r, int g, int b, int a) {
        if (index >= 0 && index < vertexArray->getVertexCount()) {
            (*vertexArray)[index].color = sf::Color(r, g, b, a);
        }
    }

    MOON_API void
    _VertexArray_SetAllVerticesColor(VertexArrayPtr vertexArray, int r, int g, int b, int a) {
        sf::Color color(r, g, b, a);
        for (size_t i = 0; i < vertexArray->getVertexCount(); ++i) {
            (*vertexArray)[i].color = color;
        }
    }

    // Функции для работы с текстурными координатами
    MOON_API void
    _VertexArray_AddVertexWithTexCoords(VertexArrayPtr vertexArray, float x, float y, int r, int g, int b, int a, float texX, float texY) {
        vertexArray->append(sf::Vertex(
            sf::Vector2f(x, y),
            sf::Color(r, g, b, a),
            sf::Vector2f(texX, texY)
        ));
    }

    MOON_API void
    _VertexArray_SetVertexTexCoords(VertexArrayPtr vertexArray, int index, float texX, float texY) {
        if (index >= 0 && index < vertexArray->getVertexCount()) {
            (*vertexArray)[index].texCoords = sf::Vector2f(texX, texY);
        }
    }

    MOON_API void
    _VertexArray_SetQuadTexCoords(VertexArrayPtr vertexArray, int startIndex, float left, float top, float width, float height) {
        if (startIndex >= 0 && startIndex + 3 < vertexArray->getVertexCount()) {
            (*vertexArray)[startIndex].texCoords = sf::Vector2f(left, top);
            (*vertexArray)[startIndex + 1].texCoords = sf::Vector2f(left + width, top);
            (*vertexArray)[startIndex + 2].texCoords = sf::Vector2f(left + width, top + height);
            (*vertexArray)[startIndex + 3].texCoords = sf::Vector2f(left, top + height);
        }
    }

    // Специальная функция для отрисовки VertexArray с RenderStates
    MOON_API void _Window_DrawVertexArrayWithRenderStates(sf::RenderWindow* window, sf::RenderStates* render_states, VertexArrayPtr vertexArray) {
        window->draw(*vertexArray, *render_states);
    }
}

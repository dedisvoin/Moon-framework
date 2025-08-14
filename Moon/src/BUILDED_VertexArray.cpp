#ifndef SFML_GRAPHICS_HPP
#include "SFML/Graphics.hpp"
#endif 

extern "C" {

    typedef sf::VertexArray* VertexArrayPtr;

    __declspec(dllexport) VertexArrayPtr 
    _VertexArray_Create() {
        return new sf::VertexArray();
    }

    __declspec(dllexport) void 
    _VertexArray_Delete(VertexArrayPtr vertexArray) {
        delete vertexArray;
    }

    __declspec(dllexport) void 
    _VertexArray_AddVertexForPositionAndColor(VertexArrayPtr vertexArray, double x, double y, int r, int g, int b, int a) {
        vertexArray->append(sf::Vertex(sf::Vector2f(static_cast<float>(x), static_cast<float>(y)), sf::Color(static_cast<sf::Uint8>(r), static_cast<sf::Uint8>(g), static_cast<sf::Uint8>(b), static_cast<sf::Uint8>(a))));
    }

    __declspec(dllexport) void 
    _VertexArray_SetPrimitiveType(VertexArrayPtr vertexArray, int primitiveType) {
        vertexArray->setPrimitiveType(static_cast<sf::PrimitiveType>(primitiveType));
    }

    __declspec(dllexport) void 
    _VertexArray_Resize(VertexArrayPtr vertexArray, int vertexCount) {
        vertexArray->resize(static_cast<size_t>(vertexCount));
    }

    __declspec(dllexport) void 
    _VertexArray_Clear(VertexArrayPtr vertexArray) {
        vertexArray->clear();
    }

    __declspec(dllexport) int
    _VertexArray_GetVertexCount(VertexArrayPtr vertexArray) {
        return static_cast<int>(vertexArray->getVertexCount());
    }

    __declspec(dllexport) float
    _VertexArray_GetVertexPositionX(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0.0f; 
        return vertexArray->operator[](index).position.x;
    }

    __declspec(dllexport) float
    _VertexArray_GetVertexPositionY(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0.0f; 
        return vertexArray->operator[](index).position.y;
    }
        
    __declspec(dllexport) int
    _VertexArray_GetVertexColorR(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.r;
    }
    
    __declspec(dllexport) int
    _VertexArray_GetVertexColorG(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.g;
    }

    __declspec(dllexport) int
    _VertexArray_GetVertexColorB(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0;
        return vertexArray->operator[](index).color.b;
    }
        
    __declspec(dllexport) int
    _VertexArray_GetVertexColorA(VertexArrayPtr vertexArray, int index) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return 0; 
        return vertexArray->operator[](index).color.a;
    }


    __declspec(dllexport) void
    _VertexArray_SetVertexForPositionAndColor(VertexArrayPtr vertexArray, int index, double x, double y, int r, int g, int b, int a) {
        if (index < 0 || index >= vertexArray->getVertexCount()) return; 
        vertexArray->operator[](index) = sf::Vertex(sf::Vector2f(static_cast<float>(x), static_cast<float>(y)), sf::Color(static_cast<sf::Uint8>(r), static_cast<sf::Uint8>(g), static_cast<sf::Uint8>(b), static_cast<sf::Uint8>(a)));
    }

    __declspec(dllexport) int 
    _VertexArray_GetPrimitiveType(VertexArrayPtr vertexArray) {
        return static_cast<int>(vertexArray->getPrimitiveType());
    }
}

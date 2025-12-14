#include "SFML/Graphics/Color.hpp"
#include "SFML/Graphics/PrimitiveType.hpp"
#include "SFML/Graphics/VertexArray.hpp"
#include "SFML/Graphics/Vertex.hpp"
#include "SFML/System/Vector2.hpp"
#include "SFML/Graphics/ConvexShape.hpp"


#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::VertexArray* VertexArrayPtr;
typedef sf::Vertex* VertexPtr;
typedef sf::ConvexShape* ConvexShapePtr;

extern "C" {
    MOON_API VertexPtr _Vertex_Init() {
        return new sf::Vertex();
    }

    MOON_API VertexPtr _Vertex_FromPtr(VertexPtr ptr) {
        return new sf::Vertex(*ptr);
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
        // Return pointer to the vertex inside the array instead of allocating a new copy.
        // This allows Python code to modify the actual vertex stored in the array.
        return &((*array)[index]);
    }

    MOON_API void _VertexArray_RemoveVertex(VertexArrayPtr array, int index) {
        int vertexCount = array->getVertexCount();
        if (index < 0 || index >= vertexCount) return;

        for (int i = index; i < vertexCount - 1; ++i) {
            (*array)[i] = (*array)[i + 1];
        }

        array->resize(vertexCount - 1);
    }

    MOON_API void _VertexArray_InsertVertex(VertexArrayPtr array, int index, VertexPtr vertex) {
            int vertexCount = array->getVertexCount();
            if (index < 0 || index > vertexCount) return; 

            array->resize(vertexCount + 1);

            // Сдвигаем вершины от конца до позиции вставки
            for (int i = vertexCount; i > index; --i) {
                (*array)[i] = (*array)[i - 1];
            }

            (*array)[index] = *vertex;
        }

    MOON_API void _VertexArray_PrependVertex(VertexArrayPtr array, VertexPtr vertex) {
        _VertexArray_InsertVertex(array, 0, vertex);
    }

    MOON_API void _VertexArray_SetColor(VertexArrayPtr array, int r, int g, int b, int a) {
        int vertexCount = array->getVertexCount();
        for (int i = 0; i < vertexCount; ++i) {
            (*array)[i].color = sf::Color(r, g, b, a);
        }
    }
}

extern "C" {
    MOON_API ConvexShapePtr _ConvexShape_Init() {
        return new sf::ConvexShape();
    }

    MOON_API void _ConvexShape_SetPointsCount(ConvexShapePtr shape, int count) {
        shape->setPointCount(count);
    }

    MOON_API void _ConvexShape_SetPoint(const ConvexShapePtr shape, const int index, 
                                                              const double x, 
                                                              const double y) {
        shape->setPoint(index, sf::Vector2f(x, y));
    }

    MOON_API double _ConvexShape_GetPointX(const ConvexShapePtr shape, const int index) {
        return shape->getPoint(index).x;
    }

    MOON_API double _ConvexShape_GetPointY(const ConvexShapePtr shape, const int index) {
        return shape->getPoint(index).y;
    }
}
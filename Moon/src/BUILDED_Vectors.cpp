#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
    #define RESTRICT __restrict
#else
    #define MOON_API
    #define RESTRICT __restrict__
#endif

#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

class Vector2f {
public:
    double x, y;

    inline Vector2f(double x, double y) noexcept : x(x), y(y) {}

    inline Vector2f new_sum(const Vector2f& other) const noexcept {
        return Vector2f(x + other.x, y + other.y);
    }

    inline Vector2f new_sub(const Vector2f& other) const noexcept {
        return Vector2f(x - other.x, y - other.y);
    }

    inline Vector2f new_mul(double scalar) const noexcept {
        return Vector2f(x * scalar, y * scalar);
    }

    inline Vector2f new_mul_vector(const Vector2f& other) const noexcept {
        return Vector2f(x * other.x, y * other.y);
    }

    inline Vector2f new_div(double scalar) const noexcept {
        return Vector2f(x / scalar, y / scalar);
    }

    inline Vector2f new_div_vector(const Vector2f& other) const noexcept {
        return Vector2f(x / other.x, y / other.y);
    }

    inline void sum(const Vector2f& other) noexcept {
        x += other.x; y += other.y;
    }

    inline void sub(const Vector2f& other) noexcept {
        x -= other.x; y -= other.y;
    }

    inline void mul(double scalar) noexcept {
        x *= scalar; y *= scalar;
    }

    inline void mul_vector(const Vector2f& other) noexcept {
        x *= other.x; y *= other.y;
    }

    inline void div(double scalar) noexcept {
        x /= scalar; y /= scalar;
    }

    inline void div_vector(const Vector2f& other) noexcept {
        x /= other.x; y /= other.y;
    }

    inline void normalize() noexcept {
        double len = length();
        if (len != 0) { x /= len; y /= len; }
    }

    inline double length() const noexcept {
        return std::sqrt(x * x + y * y);
    }

    inline void rotate_at(double angle) noexcept {
        double rad = angle * (M_PI / 180.0);
        double cos_a = std::cos(rad);
        double sin_a = std::sin(rad);
        double nx = x * cos_a - y * sin_a;
        double ny = x * sin_a + y * cos_a;
        x = nx; y = ny;
    }

    inline Vector2f rotate(double angle) const noexcept {
        double rad = angle * (M_PI / 180.0);
        double cos_a = std::cos(rad);
        double sin_a = std::sin(rad);
        return Vector2f(x * cos_a - y * sin_a, x * sin_a + y * cos_a);
    }
};

extern "C" {
    typedef Vector2f* Vector2fPtr;

    MOON_API Vector2fPtr _Vector2f_Create(double x, double y) noexcept {
        return new Vector2f(x, y);
    }

    MOON_API void _Vector2f_Destroy(Vector2fPtr vec) noexcept {
        delete vec;
    }

    MOON_API Vector2fPtr _Vector2f_NewSum(const Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        return new Vector2f(vec1->new_sum(*vec2));
    }

    MOON_API Vector2fPtr _Vector2f_NewSub(const Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        return new Vector2f(vec1->new_sub(*vec2));
    }

    MOON_API Vector2fPtr _Vector2f_NewMul(const Vector2fPtr RESTRICT vec, double scalar) noexcept {
        return new Vector2f(vec->new_mul(scalar));
    }

    MOON_API Vector2fPtr _Vector2f_NewMulVector(const Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        return new Vector2f(vec1->new_mul_vector(*vec2));
    }

    MOON_API Vector2fPtr _Vector2f_NewDiv(const Vector2fPtr RESTRICT vec, double scalar) noexcept {
        return new Vector2f(vec->new_div(scalar));
    }

    MOON_API Vector2fPtr _Vector2f_NewDivVector(const Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        return new Vector2f(vec1->new_div_vector(*vec2));
    }

    MOON_API void _Vector2f_Sum(Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        vec1->sum(*vec2);
    }

    MOON_API void _Vector2f_Sub(Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        vec1->sub(*vec2);
    }

    MOON_API void _Vector2f_Mul(Vector2fPtr RESTRICT vec, double scalar) noexcept {
        vec->mul(scalar);
    }

    MOON_API void _Vector2f_MulVector(Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        vec1->mul_vector(*vec2);
    }

    MOON_API void _Vector2f_Div(Vector2fPtr RESTRICT vec, double scalar) noexcept {
        vec->div(scalar);
    }

    MOON_API void _Vector2f_DivVector(Vector2fPtr RESTRICT vec1, const Vector2fPtr RESTRICT vec2) noexcept {
        vec1->div_vector(*vec2);
    }

    MOON_API void _Vector2f_NormalizeAt(Vector2fPtr RESTRICT vec) noexcept {
        vec->normalize();
    }

    MOON_API double _Vector2f_Length(const Vector2fPtr RESTRICT vec) noexcept {
        return vec->length();
    }

    MOON_API double _Vector2f_GetX(const Vector2fPtr RESTRICT vec) noexcept {
        return vec->x;
    }

    MOON_API double _Vector2f_GetY(const Vector2fPtr RESTRICT vec) noexcept {
        return vec->y;
    }

    MOON_API void _Vector2f_SetX(Vector2fPtr RESTRICT vec, double x) noexcept {
        vec->x = x;
    }

    MOON_API void _Vector2f_SetY(Vector2fPtr RESTRICT vec, double y) noexcept {
        vec->y = y;
    }

    MOON_API void _Vector2f_RotateAt(Vector2fPtr RESTRICT vec, double angle) noexcept {
        vec->rotate_at(angle);
    }

    MOON_API Vector2fPtr _Vector2f_Rotate(const Vector2fPtr RESTRICT vec, double angle) noexcept {
        return new Vector2f(vec->rotate(angle));
    }
}

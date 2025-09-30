#include "SFML/System/Clock.hpp"
#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

typedef sf::Clock* ClockPtr;

extern "C" {
    MOON_API ClockPtr createClock() {
        return new sf::Clock();
    }

    MOON_API void clockRestart(ClockPtr clock) {
        clock->restart();
    }

    MOON_API double getClockElapsedTime(ClockPtr clock) {
        return clock->getElapsedTime().asSeconds();
    }
}

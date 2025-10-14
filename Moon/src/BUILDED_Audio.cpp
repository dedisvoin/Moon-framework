

#ifndef SFML_AUDIO_HPP
#include "SFML/Audio/SoundBuffer.hpp"
#include "SFML/Audio/Sound.hpp"
#include "SFML/Audio/Music.hpp"
#endif
#ifndef IOSTREAM_H
#include <iostream>
#endif



#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

using std::cout, std::endl;
extern "C" {



    typedef sf::SoundBuffer* SoundBufferPtr;

    MOON_API SoundBufferPtr _SoundBuffer_loadFromFile(const char* path) {
        SoundBufferPtr buffer = new sf::SoundBuffer();

        if (buffer->loadFromFile(path))
            cout << "Sound: " << path << " loaded." << endl;
        else {
            cout << "Sound: " << path << "error loading sound" << endl;
        }
        return buffer;
    }

    MOON_API void _SoundBuffer_Destroy(SoundBufferPtr buffer) {
        delete buffer;
    }

    MOON_API int _SoundBuffer_GetChannelsCount(SoundBufferPtr buffer) {
        return buffer->getChannelCount();
    }

    MOON_API int _SoundBuffer_GetSampleRate(SoundBufferPtr buffer) {
        return buffer->getSampleRate();
    }
}

extern "C" {
    typedef sf::Sound* SoundPtr;

    MOON_API SoundPtr _Sound_Create(SoundBufferPtr buffer) {
        SoundPtr sound = new sf::Sound();
        sound->setBuffer(*buffer);
        return sound;
    }

    MOON_API void _Sound_Destroy(SoundPtr sound) {
        delete sound;
    }

    MOON_API void _Sound_Play(SoundPtr sound) {
        sound->play();
    }

    MOON_API void _Sound_Pause(SoundPtr sound) {
        sound->pause();
    }

    MOON_API void _Sound_Stop(SoundPtr sound) {
        sound->stop();
    }

    MOON_API void _Sound_SetLoop(SoundPtr sound, bool loop) {
        sound->setLoop(loop);
    }

    MOON_API void _Sound_SetVolume(SoundPtr sound, float volume) {
        sound->setVolume(volume);
    }

    MOON_API void _Sound_SetPitch(SoundPtr sound, float pitch) {
        sound->setPitch(pitch);
    }

    MOON_API void _Sound_SetAttenuation(SoundPtr sound, float attenuation) {
        sound->setAttenuation(attenuation);
    }

    MOON_API void _Sound_ResetBuffer(SoundPtr sound) {
        sound->resetBuffer();
    }

    MOON_API void _Sound_SetPosition(SoundPtr sound, float x, float y, float z) {
        sound->setPosition(x, y, z);
    }

    MOON_API void _Sound_SetRelativeToListener(SoundPtr sound, bool relative) {
        sound->setRelativeToListener(relative);
    }
    
    MOON_API int _Sound_GetStatus(SoundPtr sound) {
        return sound->getStatus();
    }
}

extern "C" {
    typedef sf::Music* MusicPtr;

    MOON_API MusicPtr _Music_Create(const char* path) {
        MusicPtr music = new sf::Music();
        music->openFromFile(path);
        return music;
    }

    MOON_API void _Music_Play(MusicPtr music) {
        music->play();
    }

    MOON_API void _Music_Pause(MusicPtr music) {
        music->pause();
    }

    MOON_API void _Music_Stop(MusicPtr music) {
        music->stop();
    }

    MOON_API void _Music_SetLoop(MusicPtr music, bool loop) {
        music->setLoop(loop);
    }

    MOON_API void _Music_SetVolume(MusicPtr music, float volume) {
        music->setVolume(volume);
    }

    MOON_API void _Music_SetPitch(MusicPtr music, float pitch) {
        music->setPitch(pitch);
    }

    MOON_API void _Music_SetAttenuation(MusicPtr music, float attenuation) {
        music->setAttenuation(attenuation);
    }
}
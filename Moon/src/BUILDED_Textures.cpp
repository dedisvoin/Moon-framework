#ifndef SFML_GRAPHICS_HPP
#include "SFML/Graphics.hpp"
#endif

#ifdef _WIN32
    #define MOON_API __declspec(dllexport)
#elif __linux__
    #define MOON_API
#endif

extern "C" {

    typedef sf::RenderTexture* RenderTexturePtr;

    MOON_API RenderTexturePtr
    _RenderTexture_Init() {
        return new sf::RenderTexture();
    }

    MOON_API bool
    _RenderTexture_Create(RenderTexturePtr texture, int width, int height) {
        return texture->create(width, height);
    }

    MOON_API void
    _RenderTexture_Draw(RenderTexturePtr texture, sf::Drawable* shape) {
        texture->draw(*shape);
    }

    MOON_API void
    _RenderTexture_Clear(RenderTexturePtr texture, int r, int g, int b, int a) {
        texture->clear(sf::Color(r, g, b, a));
    }

    MOON_API void
    _RenderTexture_Display(RenderTexturePtr texture) {
        texture->display();
    }

    MOON_API void
    _RenderTexture_SetSmooth(RenderTexturePtr texture, bool smooth) {
        texture->setSmooth(smooth);
    }

    MOON_API void
    _RenderTexture_DrawWithStates(RenderTexturePtr texture, sf::Drawable* shape, sf::RenderStates* states) {
        texture->draw(*shape, *states);
    }

    MOON_API void
    _RenderTexture_DrawWithShader(RenderTexturePtr texture, sf::Drawable* shape, sf::Shader* shader) {
        texture->draw(*shape, shader);
    }

    MOON_API void
    _RenderTexture_SetView(RenderTexturePtr texture, sf::View* view) {
        texture->setView(*view);
    }

    MOON_API sf::View*
    _RenderTexture_GetDefaultView(RenderTexturePtr texture) {
        return new sf::View(texture->getDefaultView());
    }

    MOON_API sf::View*
    _RenderTexture_GetView(RenderTexturePtr texture) {
        return new sf::View(texture->getView());
    }

    MOON_API sf::Texture* 
    _RenderTexture_GetTexture(RenderTexturePtr texture) {
        return new sf::Texture( texture->getTexture() );
    }

    MOON_API void
    _RenderTexture_Delete(RenderTexturePtr texture) {
        delete texture;
    }


}

extern "C" {
    typedef sf::Texture* TexturePtr;

    MOON_API TexturePtr _Texture_LoadFromFile(char* file_path) {
        TexturePtr texture = new sf::Texture();
        texture->loadFromFile(file_path);
        return texture;
    }

    MOON_API TexturePtr _Texture_LoadFromFileWithBoundRect(char* file_path, int x, int y, int w, int h) {
        TexturePtr texture = new sf::Texture();
        texture->loadFromFile(file_path, sf::IntRect(x, y ,w, h));
        return texture;
    }

    MOON_API void _Texture_Delete(TexturePtr texture) {
        delete texture;
    }

    MOON_API int _Texture_GetMaxixmumSize(TexturePtr texture) {
        return texture->getMaximumSize();
    }

    MOON_API int _Texture_GetSizeX(TexturePtr texture) {
        return texture->getSize().x;
    }

    MOON_API int _Texture_GetSizeY(TexturePtr texture) {
        return texture->getSize().y;
    }

    MOON_API void _Texture_SetRepeated(TexturePtr texture, bool value) {
        texture->setRepeated(value);
    }

    MOON_API void _Texture_SetSmooth(TexturePtr texture, bool value) {
        texture->setSmooth(value);
    }

    MOON_API void _Texture_Swap(TexturePtr texture, TexturePtr texture2) {
        texture->swap(*texture2);
    }

    MOON_API TexturePtr _Texture_SubTexture(TexturePtr texture, int x, int y, int w, int h) {
        TexturePtr subTexture = new sf::Texture();
        subTexture->loadFromImage(texture->copyToImage(), sf::IntRect(x, y, w, h));
        return subTexture;
    }
}

extern "C" {

    typedef sf::Sprite* SpritePtr;
    
    MOON_API sf::Sprite*
    _Sprite_GetFromRenderTexture(RenderTexturePtr texture) {
        return new sf::Sprite(texture->getTexture());
    }

    MOON_API SpritePtr
    _Sprite_GetFromTexture(TexturePtr texture) {
        return new sf::Sprite(*texture);
    }

    MOON_API void
    _Sprite_Scale(SpritePtr sprite, float x, float y) {
        sprite->scale(x, y);
    }

    MOON_API void
    _Sprite_Rotate(SpritePtr sprite, float angle) {
        sprite->rotate(angle);
    }

    //////////////////////////////////////////////////////////////////
    // Setters
    //////////////////////////////////////////////////////////////////
    MOON_API void
    _Sprite_SetColor(SpritePtr sprite, int r, int g, int b, int a) {
        sprite->setColor(sf::Color(r, g, b, a));
    }

    MOON_API void
    _Sprite_SetOrigin(SpritePtr sprite, float x, float y) {
        sprite->setOrigin(x, y);
    }

    MOON_API void
    _Sprite_SetPosition(SpritePtr sprite, float x, float y) {
        sprite->setPosition(x, y);
    }

    MOON_API void
    _Sprite_SetRotation(SpritePtr sprite, float angle) {
        sprite->setRotation(angle);
    }

    MOON_API void
    _Sprite_SetScale(SpritePtr sprite, float x, float y) {
        sprite->setScale(x, y);
    }

    // todo: 
    // MOON_API void
    // _Sprite_SetTexture(SpritePtr sprite) {
    // }

    //////////////////////////////////////////////////////////////////

    MOON_API int
    _Sprite_GetColorR(SpritePtr sprite) {
        return sprite->getColor().r;
    }
    
    MOON_API int
    _Sprite_GetColorG(SpritePtr sprite) {
        return sprite->getColor().g;
    }

    MOON_API int
    _Sprite_GetColorB(SpritePtr sprite) {
        return sprite->getColor().b;
    }

    MOON_API int
    _Sprite_GetColorA(SpritePtr sprite) {
        return sprite->getColor().a;
    }

    MOON_API float
    _Sprite_GetOriginX(SpritePtr sprite) {
        return sprite->getOrigin().x;
    }

    MOON_API float
    _Sprite_GetOriginY(SpritePtr sprite) {
        return sprite->getOrigin().y;
    }

    MOON_API float
    _Sprite_GetPositionX(SpritePtr sprite) {
        return sprite->getPosition().x;
    }

    MOON_API float
    _Sprite_GetPositionY(SpritePtr sprite) {
        return sprite->getPosition().y;
    }

    MOON_API float
    _Sprite_GetRotation(SpritePtr sprite) {
        return sprite->getRotation();
    }

    MOON_API float
    _Sprite_GetScaleX(SpritePtr sprite) {
        return sprite->getScale().x;
    }

    MOON_API float
    _Sprite_GetScaleY(SpritePtr sprite) {
        return sprite->getScale().y;
    }
}
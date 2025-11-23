#version 130

uniform sampler2D texture;
uniform vec2 textureSize;
uniform vec4 outlineColor = vec4(1.0, 0.0, 0.0, 1.0);
uniform float outlineThickness = 2.0;

void main()
{
    vec4 pixel = texture2D(texture, gl_TexCoord[0].xy);
    
    if (pixel.a > 0.1) {
        gl_FragColor = pixel * gl_Color;
        return;
    }
    
    vec2 onePixel = vec2(1.0, 1.0) / textureSize;
    float thickness = outlineThickness;
    
    // Проверяем только 4 направления (быстрее)
    float alpha = 0.0;
    alpha += texture2D(texture, gl_TexCoord[0].xy + vec2(onePixel.x * thickness, 0.0)).a;
    alpha += texture2D(texture, gl_TexCoord[0].xy + vec2(-onePixel.x * thickness, 0.0)).a;
    alpha += texture2D(texture, gl_TexCoord[0].xy + vec2(0.0, onePixel.y * thickness)).a;
    alpha += texture2D(texture, gl_TexCoord[0].xy + vec2(0.0, -onePixel.y * thickness)).a;
    
    if (alpha > 0.1) {
        gl_FragColor = outlineColor;
    } else {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}
#version 130

uniform sampler2D texture;
uniform vec2 textureSize;
uniform vec4 outlineColor = vec4(1.0, 0.0, 0.0, 1.0); // Красный контур по умолчанию
uniform float outlineThickness = 2.0;

void main()
{
    // Получаем текущий пиксель текстуры
    vec4 pixel = texture2D(texture, gl_TexCoord[0].xy);
    
    // Если текущий пиксель непрозрачный - рисуем как есть
    if (pixel.a > 0.1) {
        gl_FragColor = pixel * gl_Color;
        return;
    }
    
    // Вычисляем размер одного пикселя в текстурных координатах
    vec2 onePixel = vec2(1.0, 1.0) / textureSize;
    
    // Проверяем соседние пиксели на наличие непрозрачных областей
    bool hasSolidNeighbor = false;
    
    // Проверяем пиксели в радиусе outlineThickness
    for (float x = -outlineThickness; x <= outlineThickness; x++) {
        for (float y = -outlineThickness; y <= outlineThickness; y++) {
            // Пропускаем центральный пиксель (он уже прозрачный)
            if (x == 0.0 && y == 0.0) continue;
            
            // Вычисляем координаты соседнего пикселя
            vec2 neighborCoord = gl_TexCoord[0].xy + vec2(x * onePixel.x, y * onePixel.y);
            
            // Проверяем, непрозрачен ли соседний пиксель
            if (texture2D(texture, neighborCoord).a > 0.1) {
                hasSolidNeighbor = true;
                break;
            }
        }
        if (hasSolidNeighbor) break;
    }
    
    // Если есть непрозрачный сосед - рисуем контур
    if (hasSolidNeighbor) {
        gl_FragColor = outlineColor;
    } else {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0); // Прозрачный
    }
}
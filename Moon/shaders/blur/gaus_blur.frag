#version 130

uniform sampler2D texture;
uniform vec2 textureSize;
uniform float intensity; // Поставьте 1.5 или выше
uniform float radius;    // Поставьте 1.0 для начала

out vec4 fragColor;

void main()
{
    vec2 texCoord = gl_FragCoord.xy / textureSize;
    vec2 pixelSize = 1.0 / textureSize;
    
    vec4 original = texture2D(texture, texCoord);
    
    vec4 blurAccum = vec4(0.0);
    float totalWeight = 0.0;
    
    // НАСТРОЙКА РАЗБРОСА
    // Это аналог вашего старого "* 8". 
    // Увеличьте это число (3.0, 5.0, 8.0), если свечение слишком узкое.
    float spread = 10.0; 
    
    // Цикл 9x9 (от -4 до 4)
    for (int x = -10; x <= 10; x++) {
        for (int y = -10; y <= 10; y++) {
            // Считаем смещение
            vec2 offset = vec2(float(x), float(y));
            
            // Упрощенный расчет веса (чем дальше, тем меньше вес)
            // 1.0 / distance - дает очень сильный "звездный" ореол
            float dist = dot(offset, offset);
            float weight = exp(-dist / (2.0 * radius * radius)); // Гаусс
            
            // Смещаем выборку, умножая на spread
            vec2 samplePos = texCoord + (offset * pixelSize * spread);
            
            blurAccum += texture2D(texture, samplePos) * weight;
            totalWeight += weight;
        }
    }
    
    vec4 finalBlur = blurAccum / totalWeight;
    
    // --- ОТЛАДКА ---
    // Если вы все еще не видите свечения, раскомментируйте строку ниже.
    // Вы увидите ТОЛЬКО размытие. Если экран черный - проблема не в шейдере, а в uniform-переменных.
    // fragColor = finalBlur; return;
    
    // Смешивание
    // original + (цвет размытия * силу)
    fragColor = original + (finalBlur * intensity);
}
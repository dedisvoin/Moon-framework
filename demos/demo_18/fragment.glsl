#version 430 core

// ----- Наши "Uniform" переменные -----
layout(location = 0) uniform vec2 resolution;
layout(location = 1) uniform float time;  
layout(location = 2) uniform vec2 mouse;

// ----- Функции из твоего шейдера -----
vec3 Hash23(vec2 p) {
    p = fract(p*vec2(16133.2341251, 791.43971));
    p += dot(p, p+82171.11321712);
    return abs(vec3(fract(p.x+p.y), fract(p.y-p.x), fract(p.y)));
}

vec3 Cairo(vec2 uv, float angle) {
    vec2 id = floor(uv);
    float check = mod(id.x+id.y, 2.0);
    uv = fract(uv)-0.5;
    vec2 p = abs(uv);
    if(check == 1.0) p = p.yx;
    
    float a = (angle*0.5 + 0.5)*3.1;
    vec2 n = vec2(sin(a), cos(a));
    float d = dot(p-0.5, n);
    
    if(d*(check-0.5) < 0.0)
        id.x += sign(uv.x)*0.5;
    else
        id.y += sign(uv.y)*0.5;
        
    d = min(d, p.x);
    d = max(d, -p.y);
    d = abs(d);
    d = min(d, dot(p-0.5, vec2(n.y, -n.x)));

    return vec3(id, d);
}

out vec4 fragColor;

void main()
{
    vec2 fragCoord = gl_FragCoord.xy;
    vec2 mouse_norm = mouse.xy / resolution.xy;
    
    vec2 uv = (fragCoord - 0.5 * resolution.xy) / resolution.y;
    vec3 col = vec3(0);
    
    uv *= 3.1 + mouse_norm.y * 3.0;
    uv += time * 0.1;
    
    vec3 c = Cairo(uv, 0.5 + 0.5*sin(time*0.3 + uv.x));
    
    vec3 tile_color = 0.5 + 0.5*sin(Hash23(c.xy)*6.29 + time*0.5);
    float line_color = smoothstep(0.01, 0.0, c.z-0.1);
    float line_color2 = smoothstep(0.01, 0.0, c.z-0.14);
    float gradient_color = c.z*c.z;
    
    col += gradient_color;
    col += tile_color;
    col += line_color - line_color2;

    fragColor = vec4(col, 1.0);
}
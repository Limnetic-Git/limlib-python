#version 330
in vec2 in_vert;
in vec2 in_tex;

in vec2 in_offset;
in vec2 in_size;
in float in_rotation;
in vec4 in_tint;

out vec2 v_tex;
out vec4 v_tint;

uniform mat4 u_projection;

void main()
{
    vec2 pos = (in_vert - 0.5) * in_size;
    float rad = radians(in_rotation);
    float c = cos(rad), s = sin(rad);
    pos = vec2(c * pos.x - s * pos.y, s * pos.x + c * pos.y);
    pos += in_offset;
    gl_Position = u_projection * vec4(pos, 0.0, 1.0);
    v_tex = in_tex;
    v_tint = in_tint;
}

#version 330
in vec2 v_tex;
in vec4 v_tint;
out vec4 fragColor;
uniform sampler2D u_texture;

void main()
{
    fragColor = texture(u_texture, v_tex) * v_tint;
}

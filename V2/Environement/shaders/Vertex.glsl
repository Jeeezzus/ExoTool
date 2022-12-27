#version 330

in vec3 in_vert;
in vec2 in_uv;

out vec2 fragCoord;

void main() {
    gl_Position = vec4(in_vert, 1.0f);
    fragCoord = in_uv;
}
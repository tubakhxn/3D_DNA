attribute vec3 position;
attribute vec3 normal;
attribute vec2 uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

varying vec3 vNormal;
varying vec2 vUV;

void main() {
    vNormal = normal;
    vUV = uv;
    gl_Position = projection * view * model * vec4(position, 1.0);
}

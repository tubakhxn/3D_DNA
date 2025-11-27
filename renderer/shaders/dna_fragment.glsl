precision mediump float;
varying vec3 vNormal;
varying vec2 vUV;

uniform vec3 baseColor;
uniform float time;

void main() {
    vec3 n = normalize(vNormal);
    float lighting = dot(n, normalize(vec3(0.3,0.6,0.8))) * 0.5 + 0.5;
    vec3 col = baseColor * lighting;
    gl_FragColor = vec4(col, 1.0);
}

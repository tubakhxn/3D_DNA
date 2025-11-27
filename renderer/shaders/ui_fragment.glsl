precision mediump float;
varying vec2 vTexcoord;
uniform sampler2D tex;
uniform vec4 color;
void main() {
    vec4 t = texture2D(tex, vTexcoord);
    gl_FragColor = mix(color, t, t.a);
}

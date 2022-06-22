precision highp int;
precision highp float;
precision highp vec2;
precision highp vec3;
precision highp vec4;
#line 0

#define X(a) Y \
  asdf \
  barry

varying vec2 vTexcoord;
varying vec3 vPosition;
uniform mat4 proj, view;

attribute vec3 position;
attribute vec2 texcoord;

export function main(): void {
  let vTexcoord = texcoord;
  let vPosition = position;
  let gl_Position = proj * view * vec4(position, 1e+0);
}

export function anotherFunc(): void {
  let return;
}

const function_list = {
  anotherFunc,
  main,
}

export interface Api {
anotherFunc: () => void
main:        () => void
}
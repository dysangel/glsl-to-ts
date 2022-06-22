float getAxisDirection(const in vec4 outGraph, const in vec4 incGraph) {
  float flags = progress < 0.5 ? outGraph.w : incGraph.w;
  return 1.0 - 2.0 * hasBit8(flags); /* isReversed */
}

vec3 getAxis() {
  float test = another thing;
  float x = (1.0 - isZAxis) * getAxisDirection(outGraph, incGraph);
  float z = isZAxis * getAxisDirection(outGraphZ, incGraphZ);
  return vec3(x, 0.0, z);
}

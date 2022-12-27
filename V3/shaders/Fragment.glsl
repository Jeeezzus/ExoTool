#version 330
  out vec4 fragColor; 
  in vec2 fragCoord;

  // Constants
  const int MAX_MARCHING_STEPS = 255;
  const float MIN_DIST = 0.5;
  const float MAX_DIST = 200.0;
  const float PRECISION = 0.01;
  const float EPSILON = 0.05;
  const float PI = 3.14159265359;


float satFactor=0.5;
 float movingSpeed=1.0;

  uniform float alpha01 = 0.1;
  uniform float alpha02 = 0.1;
  uniform float alpha03 = 0.1;

  uniform float alpha11 = 0.;
  uniform float alpha12 = 0.;
  uniform float alpha13 = 0.;

  uniform float alpha21 = 0.;
  uniform float alpha22 = 0.;
  uniform float alpha23 = 0.;

  uniform float alpha31 = 0.;
  uniform float alpha32 = 0.;
  uniform float alpha33 = 0.;

  uniform float alpha41 = 0.;
  uniform float alpha42 = 0.;
  uniform float alpha43 = 0.;

 
  uniform float camAngle = 0;

  float L01 = 0.4;
float L02 = 0.4;
float L03 = 0.6;

float L11 = 1.;
float L12 = 0.84;
float L13 = 0.92;

float L21 = 1.08;
float L22 = 1.04;
float L23 = 1.;

float L31 = 0.9;
float L32 = 0.9;
float L33 = 1.;

float L41 = 0.64;
float L42 = 0.6;
float L43 = 0.84;

  vec3 center1 = vec3(0.,-1.,1.);
  vec3 P11 = vec3(0.,0.,0.);
  vec3 P12 = vec3(0.,0.,0.);
  vec3 P13 = vec3(0.,0.,0.);

  vec3 center2 = vec3(0.,-1.,0.5);
  vec3 P21 = vec3(0.,0.,0.);
  vec3 P22 = vec3(0.,0.,0.);
  vec3 P23 = vec3(0.,0.,0.);

  vec3 center3 = vec3(0.,-1.,0.);
  vec3 P31 = vec3(0.,0.,0.);
  vec3 P32 = vec3(0.,0.,0.);
  vec3 P33 = vec3(0.,0.,0.);

  vec3 center4 = vec3(0.,-1.,-0.5);
  vec3 P41 = vec3(0.,0.,0.);
  vec3 P42 = vec3(0.,0.,0.);
  vec3 P43 = vec3(0.,0.,0.);

  mat3 rotateX(float theta) {
      float c = cos(theta);
      float s = sin(theta);
      return mat3(
          vec3(1, 0, 0),
          vec3(0, c, -s),
          vec3(0, s, c)
      );
  }

  mat3 rotateY(float theta) {
      float c = cos(theta);
      float s = sin(theta);
      return mat3(
          vec3(c, 0, s),
          vec3(0, 1, 0),
          vec3(-s, 0, c)
      );
  }

  mat3 rotateZ(float theta) {
      float c = cos(theta);
      float s = sin(theta);
      return mat3(
          vec3(c, -s, 0),
          vec3(s, c, 0),
          vec3(0, 0, 1)
      );
  }

  // Identity matrix.
  mat3 identity() {
      return mat3(
          vec3(1, 0, 0),
          vec3(0, 1, 0),
          vec3(0, 0, 1)
      );
  }

  struct Surface {
      float sd; // signed distance value
      vec3 col; // color
  };
  float sdRoundBox( vec3 p, vec3 b, float r )
  {
    vec3 q = abs(p) - b;
    return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0) - r;
  }
  Surface sdBox( vec3 p, vec3 b, vec3 offset, vec3 col, mat3 transform)
  {

    p = (p - offset) * transform; // apply transformation matrix
    vec3 q = abs(p) - b;
    float d = length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
    return Surface(d, col);
  }

  Surface sdFloor(vec3 p, vec3 col) {
    float d = p.y + 1.;
    return Surface(d, col);
  }

  float smin(float a, float b, float k) {
      float h = clamp(0.5 + 0.5*(a-b)/k, 0.0, 1.0);
      return mix(a, b, h) - k*h*(1.0-h);
  }

  Surface minWithColor(Surface obj1, Surface obj2) {

    return Surface(smin(obj1.sd,obj2.sd, 0.1), obj2.col);
  }

  Surface sdCapsule( vec3 p, vec3 a, vec3 b, float r , vec3 col)
  {
    vec3 pa = p - a, ba = b - a;
    float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
    return Surface(length( pa - ba*h ) - r, col);
  }

  Surface sdRoundBox( vec3 p, vec3 b, float r , vec3 col)
{
  vec3 q = abs(p) - b;
  return Surface(length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0) - r,col);
}

  Surface sdScene2(vec3 p) {
    Surface co = sdCapsule(p, vec3(0.), vec3(1.), 1., vec3(1.,1.,1.));
    return co;
  }
  vec3 color = vec3(0.12,0.1,0.1);

  Surface sdScene(vec3 p) {
    Surface co = sdCapsule(p, center1, P11, 0.2*1.3, color);
    co = minWithColor(co, sdCapsule(p, P11, P12, 0.18*1.3, color));
    co = minWithColor(co, sdCapsule(p, P12, P13, 0.16*1.3, color));
    
    co = minWithColor(co, sdCapsule(p, center2, P21, 0.19*1.3, color));
    co = minWithColor(co, sdCapsule(p, P21, P22, 0.18*1.3, color));
    co = minWithColor(co, sdCapsule(p, P22, P23, 0.175*1.3, color));
    
    co = minWithColor(co, sdCapsule(p, center3, P31, 0.18*1.3, color));
    co = minWithColor(co, sdCapsule(p, P31, P32, 0.17*1.3, color));
    co = minWithColor(co, sdCapsule(p, P32, P33, 0.16*1.3, color));
    
    co = minWithColor(co, sdCapsule(p, center4, P41, 0.16*1.3, color));
    co = minWithColor(co, sdCapsule(p, P41, P42, 0.15*1.3, color));
    co = minWithColor(co, sdCapsule(p, P42, P43, 0.15*1.3, color));
    co = minWithColor(co, sdRoundBox(p + vec3(-0.1,2.1,-0.2), vec3(0.000000001,1.,0.75), 0.3, color));
    return co;
  }

  Surface rayMarch(vec3 ro, vec3 rd, float start, float end) {
    float depth = start;
    Surface co; // closest object

    for (int i = 0; i < MAX_MARCHING_STEPS; i++) {
      vec3 p = ro + depth * rd;
      co = sdScene(p);
      depth += co.sd;
      if (co.sd < PRECISION || depth > end) break;
    }
    
    co.sd = depth;
    
    return co;
  }

  vec3 calcNormal(in vec3 p) {
      vec2 e = vec2(1, -1) * EPSILON;
      return normalize(
        e.xyy * sdScene(p + e.xyy).sd +
        e.yyx * sdScene(p + e.yyx).sd +
        e.yxy * sdScene(p + e.yxy).sd +
        e.xxx * sdScene(p + e.xxx).sd);
  }


  mat3 camera(vec3 cameraPos, vec3 lookAtPoint) {
    vec3 cd = normalize(lookAtPoint - cameraPos); // camera direction
    vec3 cr = normalize(cross(vec3(0, 1, 0), cd)); // camera right
    vec3 cu = normalize(cross(cd, cr)); // camera up
    
    return mat3(-cr, cu, -cd);
  }

  void main()
  {

  P11 = vec3(L11*cos(alpha11),L11*sin(alpha11),0.) + center1;
P12 = vec3(L12*cos(alpha12),L12*sin(alpha12),0.) + P11;
P13 = vec3(L13*cos(alpha13),L13*sin(alpha13),0.) + P12;

P21 = vec3(L21*cos(alpha21),L21*sin(alpha21),0.) + center2;
P22 = vec3(L22*cos(alpha22),L22*sin(alpha22),0.) + P21;
P23 = vec3(L23*cos(alpha23),L23*sin(alpha23),0.) + P22;

P31 = vec3(L31*cos(alpha31),L31*sin(alpha31),0.) + center3;
P32 = vec3(L32*cos(alpha32),L32*sin(alpha32),0.) + P31;
P33 = vec3(L33*cos(alpha33),L33*sin(alpha33),0.) + P32;

P41 = vec3(L41*cos(alpha41),L41*sin(alpha41),0.) + center4;
P42 = vec3(L42*cos(alpha42),L42*sin(alpha42),0.) + P41;
P43 = vec3(L43*cos(alpha43),L43*sin(alpha43),0.) + P42;
    vec2 uv = fragCoord;

    vec3 backgroundColor1 = vec3(0.8 ,0.8,0.83);

    vec3 col = vec3(0.);
    vec3 lp = vec3(vec3(cos(camAngle), -0., sin(camAngle))); // lookat point (aka camera target)
    vec3 ro = vec3(0., 0., 0.); // ray origin that represents camera position
    
    float cameraRadius = 3.25;
    ro.x = cameraRadius * (lp.x + ro.x); // convert to polar 
    ro.z = cameraRadius * (lp.z + ro.z);
    ro.y = cameraRadius * (lp.y + ro.y);
    
    vec3 rd = camera(ro, lp) * normalize(vec3(uv, -1)); // ray direction

    Surface co = rayMarch(ro, rd, MIN_DIST, MAX_DIST); // closest object

    if (co.sd > MAX_DIST) {
      col =  backgroundColor1;
    } else {
      vec3 p = ro + rd * co.sd;
      vec3 normal = calcNormal(p);
      vec3 lightPosition = vec3(-1., 3., 0.);
      vec3 lightDirection = normalize(lightPosition - p);
      vec3 lightPosition3 = vec3(0., -1., 0.);
      vec3 lightDirection3 = normalize(lightPosition - p);
      vec3 lightPosition2 = vec3(-0, -4, 1);
      vec3 lightDirection2 = normalize(lightPosition2 - p);

      float dif = clamp(dot(normal, lightDirection), 0.7, 100.);
      float dif2 = clamp(dot(normal, lightDirection2), 0.7, 100.);
      float dif3 = clamp(dot(normal, lightDirection3), 0.7, 200.);

      col = ((3*dif3) * (2* dif) * (2 * dif2) * (co.col))/2;
      //col = (dif * dif2 * (co.col));
      //col = dif2 * co.col;
      //col = co.col;
    }

    fragColor = vec4(col, 1.0);
  }
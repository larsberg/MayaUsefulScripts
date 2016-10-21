# pointInTriangle.py

def pointInTriangle(t0, t1, t2, u, v):
  
  if ( u + v ) > 1:
    u = 1.0 - u;
    v = 1.0 - v;

  return t0 * u + t1 * v + t2 * (1 - u - v);

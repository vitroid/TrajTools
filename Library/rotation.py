#!/usr/bin/env python
# coding: utf-8
from math import *
import sys

#should be rewritten with numpy

def sqlen(v):
    s=0.0
    for k in range(3):
        s += v[k]**2
    return s
    
def normalize(v):
    r=1.0 / sqrt(sqlen(v))
    return v[0]*r,v[1]*r,v[2]*r

def decide1(x1,y1,z1,x2,y2,z2,x3,y3,z3):
    x4=-(x1+x2+x3)
    y4=-(y1+y2+y3)
    z4=-(z1+z2+z3)
    return normalize(x4,y4,z4)


def decide2(x1,y1,z1,x2,y2,z2):
    dx,dy,dz=normalize(x1+x2,y1+y2,z1+z2)
    vx,vy,vz=normalize(y1*z2-z1*y2,z1*x2-x1*z2,x1*y2-y1*x2)
    dx*=-sqrt(1./3)
    dy*=-sqrt(1./3)
    dz*=-sqrt(1./3)
    vx *= sqrt(2./3)
    vy *= sqrt(2./3)
    vz *= sqrt(2./3)
    return dx+vx,dy+vy,dz+vz,dx-vx,dy-vy,dz-vz



#outer product of two vectors; return None if vector is too small
def op(i,j,check=True):
    if check and (sqlen(i) < 0.01 or sqlen(j) < 0.01):
        return None
    a = [0.0] * 3
    for k in range(3):
        a[k] = i[k-2]*j[k-1] - i[k-1]*j[k-2]
    if check and sqlen(a) < 0.01:
        return None
    return a


def ip(i,j):
    cosine = 0.0
    for k in range(3):
        cosine += i[k]*j[k]
    return cosine


#calculate quaternions from a rotation matrix (three orthogonal vectors)
def rotmat2quat(mat):
    i = (mat[0],mat[3],mat[6])
    j = (mat[1],mat[4],mat[7])
    k = (mat[2],mat[5],mat[8])
    #print sqlen(i),sqlen(j),sqlen(k)
    
    # i軸をx軸に移す回転の軸は、iとxの2分面上にある。
    # j軸をy軸に移す回転の軸は、jとyの2分面上にある。
    # そして、それらを同時にみたす回転の軸は、2つの2分面の交線である。
    # 交線は、2つの面の法線のいずれとも直交する=外積である。*/
    
    a = op((i[0]-1.0,i[1],i[2]),(j[0],j[1]-1.0,j[2]))
    if not a:
        a = op((i[0]-1.0,i[1],i[2]),(k[0],k[1],k[2]-1.0))
        if not a:
            a = op((k[0],k[1],k[2]-1.0),(j[0],j[1]-1.0,j[2]))
            if not a:
                sys.stderr.write("outer prod warning\n")
                #//全く回転しないケース
                return 1.0, 0.0, 0.0, 0.0
    a = normalize(a)
    
    #/*回転軸aが求まったので、x軸をi軸に重ねる回転の大きさを求める。。*/
    x0 = 1.0 -a[0]*a[0], 0.0 -a[0]*a[1], 0.0 -a[0]*a[2]
    i0 = i[0]-a[0]*a[0], i[1]-a[0]*a[1], i[2]-a[0]*a[2]
    if sqlen(i0) < 0.01:
        i0 = j[0]-a[1]*a[0], j[1]-a[1]*a[1], j[2]-a[1]*a[2]
        x0 = 0.0 -a[1]*a[0], 1.0 -a[1]*a[1], 0.0 -a[1]*a[2]

    i0 = normalize(i0)
    x0 = normalize(x0)
    cosine = ip(i0,x0)
    if cosine < -1.0 or cosine > 1.0:
        cosh = 0.0
        sinh = 1.0
    else:
        cosh=sqrt((1.0+cosine)*0.5)
        sinh=sqrt(1.0-cosh*cosh)
    #//fprintf(stderr,"sinh %24.17e %24.17e %24.17e\n",cosine,cosh,sinh);
    #/*outer product to determine direction*/
    o = op(i0,x0,False)
    if ip(o,a) < 0.0:
        sinh=-sinh;
    
    return cosh, -sinh*a[0], +sinh*a[1], -sinh*a[2]



def quat2rotmat(q):
    a,b,c,d = q
    sp11=(a*a+b*b-(c*c+d*d))
    sp12=-2.0*(a*d+b*c)
    sp13=2.0*(b*d-a*c)
    sp21=2.0*(a*d-b*c)
    sp22=a*a+c*c-(b*b+d*d)
    sp23=-2.0*(a*b+c*d)
    sp31=2.0*(a*c+b*d)
    sp32=2.0*(a*b-c*d)
    sp33=a*a+d*d-(b*b+c*c)
    return sp11,sp12,sp13, sp21,sp22,sp23, sp31,sp32,sp33



def euler2quat(e):
    ea,eb,ec = e
    a=cos(ea/2)*cos((ec+eb)/2)
    b=sin(ea/2)*cos((ec-eb)/2)
    c=sin(ea/2)*sin((ec-eb)/2)
    d=cos(ea/2)*sin((ec+eb)/2)
    return a,b,c,d
    


def quat2euler(q):
    e = [0.0] * 3
    if q[0] == 1.0:
        return e
    p = 2*(q[0]**2+q[3]**2) - 1
    if p>1.0:
        p=1.0
    if p<-1.0:
        p=-1.0
    e[0] = acos(p)
    thh = e[0] / 2.0
    sinthh = sin(thh)
    costhh = cos(thh)
    p = q[0]/costhh
    if p>1.0:
        p=1.0
    if p<-1.0:
        p=-1.0
    p = acos(p)
    if sinthh == 0.0:
        s = 1.0
    else:
        s = q[1]/sinthh
    if s>1.0:
        s=1.0
    if s<-1.0:
        s=-1.0
    s=acos(s)
    if q[3]<0.0:
        p=2*pi-p
    if q[2]>0:
        e[2] = p+s
        e[1] = p-s
    else:
        e[2] = p-s
        e[1] = p+s
    return e


def qadd(q1,q2):
    a1,b1,c1,d1 = q1
    a2,b2,c2,d2 = q2
    a3=a1*a2-b1*b2-c1*c2-d1*d2
    b3=a1*b2+b1*a2+c1*d2-d1*c2
    c3=a1*c2+c1*a2-b1*d2+d1*b2
    d3=a1*d2+d1*a2+b1*c2-c1*b2
    if a3 < 0:
       a3 = -a3
       b3 = -b3
       c3 = -c3
       d3 = -d3
    return (a3,b3,c3,d3)



def test_rotation():
    e = (0.2,0.3,0.4)
    print e
    print quat2euler(euler2quat(e))
    print euler2quat(e)
    print rotmat2quat(quat2rotmat(euler2quat(e)))


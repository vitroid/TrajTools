#!/usr/bin/env python
# coding: utf-8
from math import *
import sys
import numpy
import numpy.linalg

#rewritten with numpy


#v1,v2,v3: numpy arrays
#return value: fourth vector candidate
def decide1(v1,v2,v3):
    v4 = -(v1+v2+v3)
    return v4 / numpy.linalg.norm(v4)


def decide2(v1,v2):
    d = v1+v2
    d /= numpy.linalg.norm(d)
    v = numpy.cross(v1,v2)
    v /= numpy.linalg.norm(v)
    d *= -sqrt(1./3)
    v *=  sqrt(2./3)
    return d+v,d-v


#outer product of two vectors; return None if vector is too small
def op(i,j,check=True):
    if check and (numpy.linalg.norm(i) < 0.1 or numpy.linalg.norm(j) < 0.1):
        return numpy.array([])
    a = numpy.cross(i,j)
    if check and numpy.linalg.norm(a) < 0.1:
        return numpy.array([])
    return a



#calculate quaternions from a rotation matrix (three orthogonal vectors)
def rotmat2quat0(i,j,k):
    #print sqlen(i),sqlen(j),sqlen(k)
    ex = numpy.array((1.0, 0.0, 0.0))
    ey = numpy.array((0.0, 1.0, 0.0))
    ez = numpy.array((0.0, 0.0, 1.0))
    
    # i軸をx軸に移す回転の軸は、iとxの2分面上にある。
    # j軸をy軸に移す回転の軸は、jとyの2分面上にある。
    # そして、それらを同時にみたす回転の軸は、2つの2分面の交線である。
    # 交線は、2つの面の法線のいずれとも直交する=外積である。*/
    
    a = op(i-ex, j-ey)
    if a.size == 0:
        a = op(i-ex, k-ez)
        if a.size == 0:
            a = op(k-ez, j-ey)
            if a.size == 0:
                sys.stderr.write("outer prod warning\n")
                #//全く回転しないケース
                return 1.0, 0.0, 0.0, 0.0
    a /= numpy.linalg.norm(a)
    #/*回転軸aが求まったので、x軸をi軸に重ねる回転の大きさを求める。。*/
    x0 = ex - a[0]*a
    i0 = i  - a[0]*a
    if numpy.linalg.norm(i0) < 0.1:
        i0 = j - a[1]*a
        x0 = ey - a[1]*a

    i0 /= numpy.linalg.norm(i0)
    x0 /= numpy.linalg.norm(x0)
    cosine = numpy.dot(i0,x0.transpose())
    if cosine < -1.0 or cosine > 1.0:
        cosh = 0.0
        sinh = 1.0
    else:
        cosh=sqrt((1.0+cosine)*0.5)
        sinh=sqrt(1.0-cosh*cosh)
    #//fprintf(stderr,"sinh %24.17e %24.17e %24.17e\n",cosine,cosh,sinh);
    #/*outer product to determine direction*/
    o = op(i0,x0,False)
    a = a.transpose()
    if numpy.dot(o,a) < 0.0:
        sinh=-sinh;
    
    return numpy.array((cosh, -sinh*a[0], +sinh*a[1], -sinh*a[2]))



def rotmat2quat(m):
    print "rotmat2quat is not reliable yet."
    sys.exit(1)
    n = m.transpose()
    return rotmat2quat0(numpy.array(n[0]),numpy.array(n[1]),numpy.array(n[2]))


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
    return numpy.matrix([[sp11,sp12,sp13], [sp21,sp22,sp23], [sp31,sp32,sp33]])



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
    return numpy.array([a3,b3,c3,d3])



def qmul(q,x):
    if q[0] >= 1.0:
        return numpy.array(q)
    phi = acos(q[0])
    sine = sqrt(1.0-q[0]**2)
    if q[1] < 0:
        phi=-phi
        sine=-sine
    phi *= x
    sine = sin(phi) / sine
    a = numpy.zeros(4)
    a[0] = cos(phi)
    a[1] = q[1]*sine
    a[2] = q[2]*sine
    a[3] = q[3]*sine
    return a


def test_rotation():
    e = (0.2,0.3,0.4)
    print e
    print quat2euler(euler2quat(e))
    print euler2quat(e)
    print rotmat2quat(quat2rotmat(euler2quat(e)))
    q = euler2quat(e)
    q = qmul(q, 0.5)
    print qadd(q,q)


    

def test():
    """Testing Docstring"""
    pass

if __name__=='__main__':
    q1 = numpy.array([0.5,0.5,0.5,0.5]);
    q2 = numpy.array([0.5,0.5,0.5,-0.5]);
    q21 = qadd(q2,qmul(q1,-1))
    print q21
    print qadd(q21,q1)
    q3 = numpy.array([0.60876143, -0.45804276,  0.45804276, -0.45804276])
    print qadd(q3,q1)
    print qadd(q1,q3)
    

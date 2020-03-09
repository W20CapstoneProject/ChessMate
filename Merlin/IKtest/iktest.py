from numpy import radians, degrees
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt
import matplotlib.pyplot as pyplot

l1 = 220
l2 = 220
l3 = 95

sigma = 1

def forward(o1, o2, o3):
    x = l1*cos(o1) + l2*cos(o1+o2) + l3*cos(o1+o2+o3)
    y = l1*sin(o1) + l2*sin(o1+o2) + l3*sin(o1+o2+o3)
    phi = (o1 + o2 + o3)
    return x,y,phi

def solve2R(x, y):
    #r =  sqrt(x*x + y*y)
    theta2 = (sigma)*acos((x*x + y*y - l1*l1 - l2*l2)/(2*l1*l2))
    theta1 = atan(y/x) - atan((l2*sin(theta2))/(l1+l2*cos(theta2)))
    return theta1, theta2

def inverse(x, y, phi):
    x3 = x-l3*cos(phi)
    y3 = y-l3*sin(phi)
    o1,o2 = solve2R(x3, y3)
    o3 = phi - o1 - o2
    return [o1, o2, o3]

def plotxy(n, m):
    xs = list()
    ys = list()
    x1 = list()
    x2 = list()
    x3 = list()
    for i in range(0, 180):
        if (i < n):
            x1.append(radians(i))
        if (i < m):
            x2.append(radians(i))
        x3.append(radians(i))   
    for o1 in x1:
        for o2 in x2:
            for o3 in x3:       
                x,y,phi = forward(o1,o2,o3)
                if((x>0) and (y>0)):
                    xs.append(x)
                    ys.append(y)   
    pyplot.scatter(ys,xs)
    pyplot.show()
                

if __name__ == '__main__':
    pass
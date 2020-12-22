#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x1 == x0:
            k = None
        else:
            k = (y1 - y0) / (x1 - x0)
        if (k == None and y0 > y1) or (k != None and ((abs(k) < 1 and x0 > x1) or (abs(k) >= 1 and y0 > y1))):
            x0, y0, x1, y1 = x1, y1, x0, y0
        if abs(x1-x0) >= abs(y1-y0):#choose the longer side to use the step of 1
            length = abs(x1-x0)
        else:
            length = abs(y1-y0)
        if k == None:
            d_x = 0
        else:
            if length == 0:
                return result
            d_x = (x1-x0) / length
        if length == 0:
            return result
        d_y = (y1-y0) / length
        result.append((x0,y0))
        x = x0 + 0.5
        y = y0 + 0.5 #plus 0.5 for correct round off
        i = 0
        while(i != length):
            result.append((int(x),int(y)))
            if k == None or abs(k) >= 1:
                y += 1
                x += d_x
            else:
                x += 1
                y += d_y
            i += 1
        result.append((int(x1), int(y1)))
    elif algorithm == 'Bresenham':
        if x0 == x1:
            k = None
        else:
            k = (y0-y1) / (x0-x1)
        if (k == None and y0 > y1) or (k != None and ((abs(k) <= 1 and x0 > x1) or (abs(k) > 1 and y0 > y1))):
            x0, y0, x1, y1 = x1, y1, x0, y0
        x = x0
        y = y0 
        result.append((x,y))
        d_x = x1 - x0
        d_y = y1 - y0
        if k != None and abs(k) <= 1:
            if k >= 0:
                p_k = - d_x + 2*d_y
            else:
                p_k = d_x + 2*d_y
            i = 0
            while i != d_x:
                if k >= 0:
                    if p_k >= 0:
                        y += 1
                        p_k += (2*d_y-2*d_x)
                    else:
                        p_k += 2*d_y
                else:
                    if p_k <= 0:
                        y -= 1
                        p_k += (2*d_y+2*d_x)
                    else:
                        p_k += 2*d_y
                x += 1
                result.append((x,y))
                i += 1
        else:
            if k != None and k >= 0:
                p_k = -d_y+2*d_x
            else:
                p_k = d_y+2*d_x
            i = 0
            while i != d_y:
                if k != None and k >= 0:
                    if p_k >= 0:
                        x += 1
                        p_k += (-2*d_y+2*d_x)
                    else:
                        p_k += 2*d_x
                else:
                    if k != None and p_k <= 0:
                        x -= 1
                        p_k += 2*d_y+2*d_x
                    else:
                        p_k += 2*d_x
                y += 1
                result.append((x,y))
                i += 1
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    x_mid = (x0+x1) / 2
    y_mid = (y0+y1) / 2
    a = abs(x0 - x_mid)
    b = abs(y0 - y_mid)
    x = 0
    y = b
    result.append((int(x + x_mid),int(y + y_mid)))
    result.append((int(x + x_mid),int(y_mid - y)))
    p = b*b - a*a*b + a*a/4
    while b*b*x < a*a*y:
        if p < 0:
            p += 2*b*b*x + 3*b*b
        else:
            p += 2*b*b*x - 2*a*a*y + 2*a*a + 3*b*b
            y -= 1
        x += 1
        result.append((int(x + x_mid),int(y + y_mid)))
        result.append((int(-x + x_mid),int(y + y_mid)))
        result.append((int(x + x_mid),int(-y + y_mid)))
        result.append((int(-x + x_mid),int(-y + y_mid)))
    p = b*b*(x+1/2)*(x+1/2)+a*a*(y-1)*(y-1)-a*a*b*b
    while y > 0:
        if p <= 0:
            p += 2*b*b*x - 2*a*a*y + 2*b*b + 3*a*a
            x += 1
        else:
            p += -2*a*a*y + 3*a*a
        y -= 1
        result.append((int(x + x_mid),int(y + y_mid)))
        result.append((int(-x + x_mid),int(y + y_mid)))
        result.append((int(x + x_mid),int(-y + y_mid)))
        result.append((int(-x + x_mid),int(-y + y_mid)))
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    step = 1.0 / 10000#精度
    if algorithm == 'Bezier':
        n = len(p_list)
        list_x = [0]*(n-1)
        list_y = [0]*(n-1)
        x, y = p_list[0]
        t = 0.0
        while t <= 1:
            i = 1
            while i <= n:
                j = 0
                while j < (n - i):
                    if i == 1:#the first time
                        list_x[j] = (1-t)*p_list[j][0] + t*p_list[j+1][0]
                        list_y[j] = (1-t)*p_list[j][1] + t*p_list[j+1][1]
                    else:
                        list_x[j] = (1-t)*list_x[j] + t*list_x[j+1]
                        list_y[j] = (1-t)*list_y[j] + t*list_y[j+1]
                    j+=1
                i+=1
            result.append((int(x),int(y)))
            x = list_x[0]
            y = list_y[0]
            t += step
    elif algorithm == 'B-spline':
        n = len(p_list)
        k = 3
        for i in range(0,n-k):
            for j in range(0,2000):
                u = float(j)/2000
                x = (1.0/6.0)*((-u*u*u+3*u*u-3*u+1)*p_list[i][0]+(3*u*u*u-6*u*u+4)*p_list[i+1][0]+(-3*u*u*u+3*u*u+3*u+1)*p_list[i+2][0]+u*u*u*p_list[i+3][0])
                y = (1.0/6.0)*((-u*u*u+3*u*u-3*u+1)*p_list[i][1]+(3*u*u*u-6*u*u+4)*p_list[i+1][1]+(-3*u*u*u+3*u*u+3*u+1)*p_list[i+2][1]+u*u*u*p_list[i+3][1])
                #print((int(x),int(y)))
                result.append((int(x),int(y)))
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in p_list:
        result.append((i[0] + dx,i[1] + dy))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in p_list:
        new_x = i[0] - x #take (x,y) as (0,0)
        new_y = i[1] - y
        res_x = new_x * math.cos(math.radians(r)) - new_y * math.sin(math.radians(r))
        res_y = new_x * math.sin(math.radians(r)) + new_y * math.cos(math.radians(r))
        result.append((int(res_x + x), int(res_y + y)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in p_list:
        new_x = i[0] - x
        new_y = i[1] - y
        result.append((int(new_x * s + x), int(new_y * s + y)))
    return result


def coding(x0, y0, x_min, y_min, x_max, y_max):
    res = 0b0000
    if x0 < x_min:
        res = res | 0b0001
    if x0 > x_max:
        res = res | 0b0010
    if y0 < y_min:
        res = res | 0b0100
    if y0 > y_max:
        res = res | 0b1000
    return res

def find_u(p1,q1,p2,q2,p3,q3,p4,q4):
    umax = 0
    umin = 1
    if p1 < 0 and umax < (q1/p1):
        umax = q1/p1
    elif p1 > 0 and umin > (q1/p1):
        umin = q1/p1
    if p2 < 0 and umax < (q2/p2):
        umax = q2/p2
    elif p2 > 0 and umin > (q2/p2):
        umin = q2/p2
    if p3 < 0 and umax < (q3/p3):
        umax = q3/p3
    elif p3 > 0 and umin > (q3/p3):
        umin = q3/p3
    if p4 < 0 and umax < (q4/p4):
        umax = q4/p4
    elif p4 > 0 and umin > (q4/p4):
        umin = q4/p4
    return [umax,umin]

def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    if p_list[0][0] <= p_list[1][0] and p_list[0][1] <= p_list[1][1]:#start with left_up
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
    elif p_list[0][0] > p_list[1][0] and p_list[0][1] > p_list[1][1]:#start with right_down
        x0, y0 = p_list[1]
        x1, y1 = p_list[0]
    elif p_list[0][0] <= p_list[1][0] and p_list[0][1] >= p_list[1][1]:#start with left_down
        x0 = p_list[0][0]
        y0 = p_list[1][1]
        x1 = p_list[1][0]
        y1 = p_list[0][1]
    elif p_list[0][0] > p_list[1][0] and p_list[0][1] < p_list[1][1]:#start with right_up
        x0 = p_list[1][0]
        y0 = p_list[0][1]
        x1 = p_list[0][0]
        y1 = p_list[1][1]
    if algorithm == 'Cohen-Sutherland':
        flag = 0 #need to break out of the loop or not
        while flag == 0:
            c1 = coding(x0,y0,x_min,y_min,x_max,y_max)
            c2 = coding(x1,y1,x_min,y_min,x_max,y_max)
            if c1&c2 != 0:
                result.append((0,0))
                result.append((0,0))
                flag = 1
            else:
                if c1|c2 == 0:
                    result.append((x0,y0))
                    result.append((x1,y1))
                    flag = 1
                else:
                    if c1 == 0:#swap, make sure (x0,y0) is always out of the block
                        x = x0
                        y = y0
                        x0 = x1
                        y0 = y1
                        x1 = x
                        y1 = y
                        c = c1
                        c1 = c2
                        c2 = c
                    #find interpoint
                    if x0 != x1:
                        k = (y0-y1) / (x0-x1)
                        b = y0 - k*x0
                    else:
                        k = None
                        b = None
                    if (c1&(0b0100)) == 0b0100:#down
                        y0 = y_min
                        if k != None:
                            x0 = int((y0-b)/k)
                    elif (c1&(0b1000)) == 0b1000:#up
                        y0 = y_max
                        if k != None:
                            x0 = int((y0-b)/k)
                    elif (c1&(0b0001)) == 0b0001:#left
                        x0 = x_min
                        y0 = int(k*x0+b)
                    elif (c1&(0b0010)) == 0b0010:#right
                        x0 = x_max
                        y0 = int(k*x0+b)
    elif algorithm == 'Liang-Barsky':
        p1 = -(x1-x0)
        q1 = x0 - x_min
        p2 = (x1-x0)
        q2 = x_max - x0
        p3 = -(y1-y0)
        q3 = y0 - y_min
        p4 = y1 - y0
        q4 = y_max - y0
        if (x1-x0) == 0:
            if q1 < 0 or q2 < 0:
                return result
            elif q1 >0 and q2 > 0:
                tmp = find_u(p1,q1,p2,q2,p3,q3,p4,q4)
                umax = tmp[0]
                umin = tmp[1]
        elif (y1-y0) == 0:
            if q3 < 0 or q4 < 0:
                return result
            elif q1 > 0 and q2 > 0:
                tmp = find_u(p1,q1,p2,q2,p3,q3,p4,q4)
                umax = tmp[0]
                umin = tmp[1]
        else:
            tmp = find_u(p1,q1,p2,q2,p3,q3,p4,q4)
            umax = tmp[0]
            umin = tmp[1]
        if umax > umin:
            return result
        elif umax < umin:
            if umax != 0:
                result.append((int(x0+umax*(x1-x0)),int(y0+umax*(y1-y0))))
            else:
                if x0>=x_min and x0<=x_max and y0>=y_min and y0<=y_max:
                    result.append((x0,y0))
                elif x1>=x_min and x1<=x_max and y1>=y_min and y1<=y_max:
                    result.append((x1,y1))
            if umin != 1:
                result.append((int(x0+umin*(x1-x0)),int(y0+umin*(y1-y0))))
            else:
                if x0>=x_min and x0<=x_max and y0>=y_min and y0<=y_max:
                    result.append((x0,y0))
                elif x1>=x_min and x1<=x_max and y1>=y_min and y1<=y_max:
                    result.append((x1,y1))
    return result
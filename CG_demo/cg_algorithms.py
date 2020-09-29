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
        k = (y1 - y0) / (x1 - x0)
        if (abs(k) < 1 and x0 > x1) or (abs(k) >= 1 and y0 > y1):
            x0, y0, x1, y1 = x1, y1, x0, y0
        if abs(x1-x0) >= abs(y1-y0):#choose the longer side to use the step of 1
            length = abs(x1-x0)
        else:
            length = abs(y1-y0)
        d_x = (x1-x0) / length
        d_y = (y1-y0) / length
        x = x0 + 0.5
        y = y0 + 0.5 #plus 0.5 for correct round off
        i = 0
        while(i != length):
            result.append((int(x),int(y)))
            if abs(k) >= 1:
                y += 1
                x += d_x
            else:
                x += 1
                y += d_y
            i += 1
    elif algorithm == 'Bresenham':
        k = (y0-y1) / (x0-x1)
        if (abs(k) < 1 and x0 > x1) or (abs(k) >=1 and y0 > y1):
            x0, y0, x1, y1 = x1, y1, x0, y0
        x = x0
        y = y0
        d_x = x1 - x0
        d_y = y1 - y0
        result.append((x,y))
        if abs(k) < 1:
            y_pre = y0
            p_k = 2*d_y - d_x
            i = 0
            while i != d_x:
                if p_k > 0:# d1>d2
                    y_pre = y
                    y += 1
                x += 1
                if i != 0 and y_pre == y:
                    p_k += 2*d_y
                elif i != 0 and y_pre + 1 == y:
                    p_k += (2*d_y-2*d_x)
                result.append((x,y))
                i += 1
        else:
            x_pre = x0
            p_k = 2*d_x - d_y
            i = 0
            while i != d_y:
                if p_k > 0:
                    x_pre = x
                    x += 1
                y += 1
                if i != 0 and x_pre == x:
                    p_k += 2*d_x
                elif i != 0 and x_pre + 1 == x:
                    p_k +=(2*d_x-2*d_y)
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
    result.append((x,y))
    p = b*b - a*a*b + a*a/4
    while b*b*x < a*a*y:
        if p < 0:
            p += 2*b*b*x + 3*b*b
        else:
            p += 2*b*b*x - 2*a*a*y + 2*a*a + 3*b*b
            y -= 1
        x += 1
        result.append((x + x_mid,y + y_mid))
        result.append((-x - x_mid,y + y_mid))
        result.append((x + x_mid,-y - y_mid))
        result.append((-x - x_mid,-y - y_mid))
    p = b*b*(x+1/2)*(x+1/2)+a*a*(y-1)*(y-1)-a*a*b*b
    while y >= 0:
        if p <= 0:
            p += -2*a*a*y + 3*a*a
            x += 1
        else:
            p += 2*b*b*x - 2*a*a*y + 2*b*b + 3*a*a
        y -= 1
        result.append((x + x_mid,y + y_mid))
        result.append((-x - x_mid,y + y_mid))
        result.append((x + x_mid,-y - y_mid))
        result.append((-x - x_mid,-y - y_mid))
    return result

    

    '''
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    x_mid = (x0+x1) / 2
    y_mid = (y0+y1) / 2
    a = abs(x0 - x_mid)
    b = abs(y0 - y_mid)
    x = 0
    y = b
    k = 0
    while abs(k) < 1:#the upper half
        y_real = math.sqrt(b*b-b*b*x*x/(a*a))
        if abs(y_real-y) > abs(y_real-(y-1)):#down side one is closer
            y -= 1
        result.append((x + x_mid,y + y_mid))
        result.append((-x - x_mid,y + y_mid))
        result.append((x + x_mid,-y - y_mid))
        result.append((-x - x_mid,-y - y_mid))
        x += 1
        k = -(b*b*x*x)/(a*a*y*y)
    x = a
    y = 0
    k = None
    while k == None or abs(k) >= 1:#the half below
        x_real = math.sqrt(a*a-a*a*y*y/(b*b))
        if abs(x_real-x) > abs(x_real - (x-1)):
            x -= 1
        result.append((x + x_mid,y + y_mid))
        result.append((-x - x_mid,y + y_mid))#for other 3 quadrants
        result.append((x + x_mid,-y - y_mid))
        result.append((-x - x_mid,-y - y_mid))
        y += 1
        k = -(b*b*x*x)/(a*a*y*y)
    return result'''



def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    pass


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
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


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
    pass

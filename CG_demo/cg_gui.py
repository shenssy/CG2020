#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QColorDialog)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QWheelEvent
from PyQt5.QtCore import QRectF
from PyQt5 import QtCore


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.color = QColor(0, 0, 0)

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    #todo

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        self.temp_id = item_id
    
    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_translate(self, item_id):
        self.temp_id = item_id
        self.temp_item = self.item_dict[self.temp_id]
        self.status = 'translate'

    def start_rotate(self, item_id):
        if self.item_dict[item_id].item_type != 'ellipse':#except ellipse
            self.temp_id = item_id
            self.status = 'rotate'
            self.temp_item = self.item_dict[self.temp_id]

    def start_scale(self, item_id):
        self.temp_id = item_id
        self.status = 'scale'
        self.temp_item = self.item_dict[self.temp_id]
    
    def start_clip(self, algorithm, item_id):
        if self.item_dict[item_id].item_type == 'line':
            self.temp_algorithm = algorithm
            self.temp_id = item_id
            self.status = 'clip'
            self.temp_item = self.item_dict[self.temp_id]

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        if selected == '':
            return
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.color)
            self.scene().addItem(self.temp_item)
        #todo
        elif self.status == 'polygon' and event.buttons () == QtCore.Qt.LeftButton:#polygon with left
            if self.temp_item != None and self.temp_item.item_type == 'polygon':
                self.temp_item.p_list.append((x,y))
            else:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.color)
                self.scene().addItem(self.temp_item)
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
        elif self.status == 'polygon' and event.buttons () == QtCore.Qt.RightButton:#polygon with right to paint
            self.temp_item = None
            self.finish_draw()
        elif self.status == 'curve' and event.buttons () == QtCore.Qt.LeftButton:
            if self.temp_item != None and self.temp_item.item_type == 'curve':
                self.temp_item.p_list.append((x,y))
            else:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.color)
                self.temp_item.curve_done = False
                self.scene().addItem(self.temp_item)
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
        elif self.status == 'curve' and event.buttons () == QtCore.Qt.RightButton:
            self.temp_item.curve_done = True
            #self.item_dict[self.temp_id] = self.temp_item
            #self.list_widget.addItem(self.temp_id)
            self.temp_item = None
            self.finish_draw()
        elif self.status == 'translate':
            self.temp_item.x_now = x
            self.temp_item.y_now = y
        elif self.status == 'rotate':
            self.temp_item.p_list = alg.rotate(self.temp_item.p_list,x,y,0)
            self.temp_item.rotate_x = x
            self.temp_item.rotate_y = y
        elif self.status == 'scale':
            self.temp_item.origin_list = self.temp_item.p_list
            self.temp_item.multiple = 1
            self.temp_item.p_list = alg.scale(self.temp_item.origin_list, x, y, self.temp_item.multiple)
            self.temp_item.scale_x = x
            self.temp_item.scale_y = y
        elif self.status == 'clip':
            self.temp_item.one_x = x
            self.temp_item.one_y = y
            self.temp_item.two_x = x
            self.temp_item.two_y = y
            self.temp_item.clip_done = False
        
        #update those unfinished curve, those b-spline curves without enough number of points will not be drawn
        for i in (self.item_dict).values():
            if i.id != self.temp_id and i.item_type == 'curve' and i.curve_done == False:
                i.curve_done = True

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line' or self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        #todo
        elif self.status == 'translate':
            self.temp_item.p_list = alg.translate(self.temp_item.p_list, x-self.temp_item.x_now,y-self.temp_item.y_now)
            self.temp_item.x_now = x
            self.temp_item.y_now = y
        elif self.status == 'clip':
            self.temp_item.two_x = x
            self.temp_item.two_y = y

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line' or self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        #todo
        elif self.status == 'clip':
            self.temp_item.clip_done = True
            self.temp_item.p_list = alg.clip(self.temp_item.p_list, self.temp_item.one_x, self.temp_item.one_y, self.temp_item.two_x, self.temp_item.two_y, self.temp_algorithm)
            self.temp_item.two_x = None
            self.temp_item.two_y = None
        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.status == 'rotate' and self.temp_item.rotate_x != None and self.temp_item.rotate_y != None:
            if event.angleDelta().y() < 0:#down
                self.temp_item.p_list = alg.rotate(self.temp_item.p_list,self.temp_item.rotate_x,self.temp_item.rotate_y,5)
            else:
                self.temp_item.p_list = alg.rotate(self.temp_item.p_list,self.temp_item.rotate_x,self.temp_item.rotate_y,355)
        elif self.status == 'scale' and self.temp_item.scale_x != None and self.temp_item.scale_y !=None:
            if event.angleDelta().y() < 0 and self.temp_item.multiple > 0:#down
                self.temp_item.multiple -= 0.05
                self.temp_item.p_list = alg.scale(self.temp_item.origin_list,self.temp_item.scale_x, self.temp_item.scale_y, self.temp_item.multiple)
            elif event.angleDelta().y() > 0:#up
                self.temp_item.multiple += 0.05
                self.temp_item.p_list = alg.scale(self.temp_item.origin_list,self.temp_item.scale_x, self.temp_item.scale_y, self.temp_item.multiple)
        self.updateScene([self.sceneRect()])
        super().wheelEvent(event)

class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', color: QColor = QColor(0, 0, 0),parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False

        self.x_now = p_list[0][0] 
        self.y_now = p_list[0][1]#for translate

        self.rotate_x = None
        self.rotate_y = None #for rotate

        self.scale_x = None
        self.scale_y = None #for scale
        self.origin_list = p_list #for scale, always use the origin points to operate
        self.multiple = 1 #original scale mutiple

        self.one_x = None
        self.one_y = None #the first point of clip
        self.two_x = None
        self.two_y = None #the second point of clip
        self.clip_done = True

        self.curve_done = True
        
        self.color = color

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(self.color)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected and len(self.p_list) == 2:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected and len(self.p_list) >= 2:
                painter.setPen(QColor(255,0,0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected and len(self.p_list) == 2:
                painter.setPen(QColor(255,0,0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve' and self.curve_done == True:
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected and len(self.p_list) > 3:
                painter.setPen(QColor(255,0,0))
                painter.drawRect(self.boundingRect())
        if self.item_type ==  'line' and self.clip_done == False and self.one_x != None and self.one_y != None and self.two_x != None and self.two_y != None:
            x1,y1,x2,y2 = alg.change(self.one_x,self.one_y,self.two_x,self.two_y)
            painter.setPen(QColor(255,0,0))
            painter.drawRect(x1,y1,x2-x1,y2-y1)
        if self.item_type == 'curve' and self.curve_done == False and len(self.p_list) >= 2:
            for i in range(len(self.p_list)-1):
                item_tmp = alg.draw_line([(self.p_list)[i],(self.p_list)[i+1]],'DDA')
                for p in item_tmp:
                    painter.setPen(QColor(255,0,0))
                    painter.drawPoint(*p)

    def boundingRect(self) -> QRectF:
        if (self.item_type == 'line' or self.item_type == 'ellipse') and len(self.p_list) != 0:
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif (self.item_type == 'polygon' or self.item_type == 'curve') and len(self.p_list) != 0:
            max_x = 0
            max_y = 0
            min_x = float('inf')
            min_y = float('inf')
            for p in self.p_list:
                if p[0] > max_x:
                    max_x = p[0]
                if p[0] < min_x:
                    min_x = p[0]
                if p[1] > max_y:
                    max_y = p[1]
                if p[1] < min_y:
                    min_y = p[1]
            return QRectF(min_x-1, min_y-1,max_x-min_x+2, max_y-min_y+2)

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        self.file_cnt = 1 #the filename of next export file

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        #todo
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        #self.list_widget.itemDoubleClicked.connect(self.canvas_widget.cancel_selection)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def set_pen_action(self):
        color = QColorDialog.getColor(self.canvas_widget.color)
        self.canvas_widget.color = color

    def reset_canvas_action(self):
        self.canvas_widget.item_dict = {}
        self.canvas_widget.selected_id = ''
        self.canvas_widget.status = '' #for back to the original status
        self.canvas_widget.color = QColor(0, 0, 0)
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        self.list_widget.clear()
        self.scene.clear()
        self.item_cnt = 0
        self.canvas_widget.temp_id = '0'
        self.statusBar().showMessage('重置画布')
    
    def save_canvas_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.item_dict[self.canvas_widget.selected_id].selected = False # save canvas without bounding rect
        fileName = str(self.file_cnt)+".bmp"
        pixmap = self.canvas_widget.grab()
        pixmap.save(fileName)
        self.file_cnt += 1
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.item_dict[self.canvas_widget.selected_id].selected = True

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def translate_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.start_translate(self.canvas_widget.selected_id)
            self.statusBar().showMessage('平移变换')
    
    def rotate_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.start_rotate(self.canvas_widget.selected_id)
            self.statusBar().showMessage('旋转变换')
    
    def scale_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.start_scale(self.canvas_widget.selected_id)
            self.statusBar().showMessage('缩放变换')
    
    def clip_cohen_sutherland_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.start_clip('Cohen-Sutherland', self.canvas_widget.selected_id)
            self.statusBar().showMessage('Cohen-Sutherland算法线段裁剪')
    
    def clip_liang_barsky_action(self):
        if self.canvas_widget.selected_id != '':
            self.canvas_widget.start_clip('Liang-Barsky', self.canvas_widget.selected_id)
            self.statusBar().showMessage('Liang-Barsky算法线段裁剪')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

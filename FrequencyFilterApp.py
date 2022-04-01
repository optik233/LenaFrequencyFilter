"""
作者：202128013920003 刘夕铭
所属机构：中国科学院长春光学精密机械与物理研究所
功能：演示图像的频域滤波
版本：Version 4
最后更改时间：2022.03.29@14.19
参考：《Understanding Optics with Python》 Vasudevan Lakshminarayanand等著，夫琅禾费衍射的UI设计
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
# QApplication 包含窗口系统和其他来源处理过和发送过的主事件循环，也处理应用程序初始化和收尾。管理对话
# QMainWindow  QMainWindow()可以创建一个应用程序的窗口。MainWindow的结构分为五个部分：菜单栏（Menu Bar）工具栏（Toolbars）、
# 停靠窗口（Dock Widgets）、状态栏（Status Bar）和中央窗口（Central Widget） 中央窗口可以使用任何形式的widget来填充
# 总结来说 QApplication 是控制模块，负责载入QT架构；； QMainWindow 是显示模块，负责把自己的UI显示出来
from PyQt5.QtCore import pyqtSlot  # 槽函数命令
from FrequencyFilterUI import Ui_MainWindow  # 把QT创建的UI界面导进来
from numpy import pi, linspace, meshgrid, sin
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
from LenaFilter import ImageFilter
import matplotlib.colorbar as colorbars


# 创建我自己的UI类，继承于QT自创的Ui_MainWindow
class FrequencyFilterApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # 主窗口初始化在自己的APP窗口上
        self.setupUi(self)  # QT生成的setupUI的函数，是UI_MainWindow里面的方法 在刚生成的主窗口上面进行我们的初始化
        self.fig1()  # 建立一个图像

    def fig1(self):
        positionx = self.SpinBoxPositionx.value()  # 接收外部波长，单位：m
        positiony = self.SpinBoxPositiony.value()  # 矩形孔的宽度，单位：m
        b = self.HorizontalSliderB.value()  # 矩形孔的高度，单位：m
        h = self.HorizontalSliderH.value()  # 菲涅尔衍射是近场衍射，传播距离，单位：m
        m = self.SpinBoxlCosm.value()  # 平面波振幅，单位：V/m
        n = self.SpinBoxlCosn.value()  # 平面波振幅，单位：V/m

        # 显示原始图像
        mpl1 = self.Lena.canvas  # 在小部件的画布上作图，创建一个小部件对象 部件名称self.mplwidget
        mpl1.ax.imshow(Lena, 'gray')  # 原图
        mpl1.ax.set_title('OriginImage')
        mpl1.ax.xaxis.set_label_position('top')
        mpl1.ax.tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                            labeltop=False, labelleft=False, labelright=False)

        # 建立Lena+Cos噪声
        z = np.cos(m * x + n * y)
        NewLena = Lena + z * 2000

        # 建立滤波对象
        ImageGroup = ImageFilter(NewLena)

        mpl2 = self.LenaPlusCos.canvas  # 建立变化画布
        mpl2.ax[0][0].clear()
        mpl2.ax[0][1].clear()
        mpl2.ax[1][0].clear()
        mpl2.ax[1][1].clear()   # 画布清空

        # Lena+Cos图像
        mpl2.ax[0][0].imshow(NewLena, 'gray')
        mpl2.ax[0][0].set_title('OriFrequency')
        mpl2.ax[0][0].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                                  labeltop=False, labelleft=False, labelright=False)

        # Lena+Cos频谱
        Spectrum = ImageGroup.Spectrum()
        mpl2.ax[0][1].imshow(np.log(1 + abs(Spectrum)), 'gray')
        mpl2.ax[0][1].set_title('OriFrequency')
        mpl2.ax[0][1].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                                  labeltop=False, labelleft=False, labelright=False)

        # Lena+Cos+RectFilter频谱
        AfterFilt = ImageGroup.Filter(Spectrum, b, h, positionx, positiony)  # 滤波频谱
        mpl2.ax[1][0].imshow(np.log(1 + abs(AfterFilt)), 'gray')
        mpl2.ax[1][0].set_title('AfterFiltFrequency')
        mpl2.ax[1][0].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                                  labeltop=False, labelleft=False, labelright=False)

        # Lena+Cos+RectFilter图像
        ArcFilter = ImageGroup.ArcFileter(AfterFilt)
        mpl2.ax[1][1].imshow(abs(ArcFilter), 'gray')
        mpl2.ax[1][1].set_title('AfterFilterImage')
        mpl2.ax[1][1].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                                  labeltop=False, labelleft=False, labelright=False)

        mpl2.draw() # 画布更新

    @pyqtSlot("int")
    def on_SpinBoxPositionx_valueChanged(self, value):
        self.HorizontalSliderPositionx.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxPositiony_valueChanged(self, value):
        self.HorizontalSliderPositiony.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxH_valueChanged(self, value):
        self.HorizontalSliderH.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxB_valueChanged(self, value):
        self.HorizontalSliderB.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxlCosm_valueChanged(self, value):
        self.HorizontalSliderCosm.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxlCosn_valueChanged(self, value):
        self.HorizontalSliderCosn.setValue(value)

    @pyqtSlot("int")
    def on_HorizontalSliderPositionx_valueChanged(self, value):
        self.SpinBoxPositionx.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_HorizontalSliderPositiony_valueChanged(self, value):
        self.SpinBoxPositiony.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_HorizontalSliderH_valueChanged(self, value):
        self.SpinBoxH.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_HorizontalSliderB_valueChanged(self, value):
        self.SpinBoxB.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_HorizontalSliderCosm_valueChanged(self, value):
        self.SpinBoxlCosm.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_HorizontalSliderCosn_valueChanged(self, value):
        self.SpinBoxlCosn.setValue(value)
        self.fig1()


if __name__ == "__main__":
    import sys

    PicturePath = './Lena.bmp'
    Lena = plt.imread(PicturePath, 'gray')  # 读图片
    SizeX = 512
    SizeY = 512
    x = np.linspace(0, SizeX, SizeX)
    y = np.linspace(0, SizeY, SizeY)
    x, y = np.meshgrid(x, y)

    app = QApplication(sys.argv)
    FrequencyFilterApp = FrequencyFilterApp()
    FrequencyFilterApp.show()  # 显示主窗口
    sys.exit(app.exec_())  # 退出

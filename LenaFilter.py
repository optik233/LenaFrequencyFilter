"""
功能：任意大小的矩形孔滤波器的频域滤波
参数：矩形原点(positionx,positiony)，矩形尺寸（b,h），控制矩形滤波器位置和尺寸。
    (positionx,positiony)=（1,1），（b,h）=（1，1）则是一个点滤波器
输出：矩形孔滤波器滤波后的图像
作者：202128013920003刘夕铭
所属机构：中国科学院长春光学精密机械与物理研究所
最后修改时间：2022.03.29@18.43
版本：Version1
类包：以矩形孔滤波器为例，还可以添加类方法如圆滤波、高斯滤波等
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


class ImageFilter:
    def __init__(self, image):
        self.image = image

    def Spectrum(self):  # 计算频谱
        ImageAfterFFT = np.fft.fft2(self.image)  # 求图像频谱
        Spectrum = np.fft.fftshift(ImageAfterFFT)  # 转移0频
        return Spectrum  # 一定要注意这里，这里只是做了0频转移

    def Filter(self, image, rect_b, rect_h, positionx, positiony):  # 滤波操作，可以添加其他的滤波器
        # if Filter == rect：
        AfterFilt = self.RectFilter(image, rect_b, rect_h, positionx, positiony)  # 矩形滤波
        # elif Filter == circle：
        #       pass
        return AfterFilt

    @staticmethod
    def ArcFileter(image):  # 计算傅里叶逆变换
        ArcFilter = np.fft.ifft2(image)  # 记住不需要再逆0频变换，因为无所谓，做变换都变回去了
        return ArcFilter

    @staticmethod
    def RectFilter(image, rect_b, rect_h, positionx, positiony):  # 创建rectFilter函数，对图像进行矩形滤波
        threshold_br = positionx + rect_b / 2
        threshold_bl = positionx - rect_b / 2
        threshold_hr = positiony + rect_h / 2
        threshold_hl = positiony - rect_h / 2  # 计算矩形的位置,原点(positionx,positiony)，宽度(b,h)
        for i in range(1, image.shape[0], 1):
            for j in range(1, image.shape[1], 1):
                if (i < threshold_br) & (i > threshold_bl) & (j < threshold_hr) & (
                        j > threshold_hl):
                    image[i][j] = 0
        return image


if __name__ == "__main__":
    # 参数初始化
    PicturePath = './Lena.bmp'
    Lena = plt.imread(PicturePath, 'gray')  # 读图片
    xtick = [-256, -192, -128, 64, 0, 64, 128, 192, 256]
    positionx = 256  # 矩形滤波的矩形原点坐标x
    positiony = 150  # 矩形滤波的矩形原点坐标y
    b = 20  # 矩形的宽
    h = 20  # 矩形的高

    # 创建cos噪声
    m, n = [Lena.shape[0], Lena.shape[1]]
    x = np.linspace(0, m, m)
    y = np.linspace(0, n, n)
    x, y = np.meshgrid(x, y)
    z = np.cos(20 * x)

    NewLena = Lena + z * 2000

    # 建立FFT变换对象
    a = ImageFilter(NewLena)

    # 开始画图
    fig, ax = plt.subplots(nrows=2, ncols=3)  # 建立画布和轴
    fig.canvas.manager.set_window_title('LenaFilter')  # 画布对象标题

    # 子图1
    plt.subplot(231)
    plt.imshow(Lena, 'gray')  # 原图
    ax[0][0].set_title('OriginImage')
    ax[0][0].xaxis.set_label_position('top')
    ax[0][0].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                         labeltop=False, labelleft=False, labelright=False)

    # 子图2
    plt.subplot(232)
    plt.imshow(NewLena, 'gray')  # 原图
    ax[0][1].set_xlabel('xDirectionPixels')  # 轴对象坐标标识
    ax[0][1].set_ylabel('yDirectionPixels')
    ax[0][1].set_title('OriginImage+cosNoise')
    ax[0][1].xaxis.set_label_position('bottom')
    ax[0][1].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                         labeltop=False, labelleft=False, labelright=False)

    # 子图3
    plt.subplot(233)
    Spectrum = a.Spectrum()  # 原图频谱
    plt.imshow(np.log(1 + abs(Spectrum)), 'gray')
    ax[0][2].set_xlabel('xDirectionFrequency')  # 轴对象坐标标识
    ax[0][2].set_ylabel('yDirectionFrequency')
    ax[0][2].set_title('OriFrequency')
    ax[0][2].xaxis.set_label_position('bottom')
    ax[0][2].yaxis.set_label_position('right')
    ax[0][2].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                         labeltop=False, labelleft=False, labelright=False)

    # 子图4
    plt.subplot(234)
    AfterFilt = a.Filter(Spectrum, b, h, positionx, positiony)  # 滤波频谱
    plt.imshow(np.log(1 + abs(AfterFilt)), 'gray')
    ax[1][0].set_xlabel('AfterFiltFrequency')  # 轴对象坐标标识
    ax[1][0].set_ylabel('AfterFiltFrequency')
    ax[1][0].set_title('AfterFiltFrequency')
    ax[1][0].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                         labeltop=False, labelleft=False, labelright=False)

    # 子图5
    plt.subplot(235)
    ArcFilter = a.ArcFileter(AfterFilt)  # 滤波图像
    plt.imshow(abs(ArcFilter), 'gray')
    ax[1][1].set_xlabel('AfterFilterX')  # 轴对象坐标标识
    ax[1][1].set_ylabel('AfterFilterY')
    ax[1][1].set_title('AfterFilterImage')
    ax[1][1].yaxis.set_label_position('left')
    ax[1][1].tick_params(axis="both", bottom=False, top=False, left=False, right=False, labelbottom=False,
                         labeltop=False, labelleft=False, labelright=False)
    # plt.gca().invert_yaxis() 翻转轴

    # 子图6
    plt.subplot(236)
    ax[1][2].set_xticks([])
    ax[1][2].set_yticks([])
    plt.plot(0)
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)
    frame.axes.get_xaxis().set_visible(False)

    plt.show()  # 显示图像结果

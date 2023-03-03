# 该代码用来数据预处理
import copy

from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

path = 'E:/LearningProjects/OCT脉络膜识别/脉络/Chr0200.png'


def lapalian_demo(image):
    #第一种方法调用算子
    #dst = cv.Laplacian(image, cv.CV_32F)
    #lpls = cv.convertScaleAbs(dst)

    #第二种方法手动实现
    kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])#定义卷积核 8邻域 还可以4邻域
    dst = cv2.filter2D(image, cv2.CV_32F, kernel=kernel)
    lpls = cv2.convertScaleAbs(dst)
    cv2.imshow("lapalian_demo", lpls)


def sobel_demo(image):
    # grad_x = cv.Sobel(image, cv.CV_32F, 1, 0)#32位float浮点数 不能使用8u 加加减减超256了。
    # grad_y = cv.Sobel(image, cv.CV_32F, 0, 1)
    grad_x = cv2.Scharr(image, cv.CV_32F, 1, 0)  #Scharr边缘增强，对弱边缘梯度提取效果好
    grad_y = cv2.Scharr(image, cv.CV_32F, 0, 1)
    gradx = cv2.convertScaleAbs(grad_x)
    grady = cv2.convertScaleAbs(grad_y)
    cv2.imshow("gradient-x", gradx)
    cv2.imshow("gradient-y", grady)

    gradxy = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)
    cv2.imshow("gradient", gradxy)


img = Image.open(path)

rows = img.height  # 860
cols = img.width   # 500
num = 0

img_array = np.array(img)  # 把图片数组化
img_array_copy = copy.copy(img_array)
mylist = []  # 存储中间最亮的几行的坐标0

for x in range(0,rows):   # 如果灰度值大于210 就认为是中间的几行 可能存在误差，可以后期加上矫正算法
    for y in range(0,cols):
        # v = img_array_copy[x,y]
        if img_array_copy[x,y] > 210:
            mylist.append([x,y])
            num = num+1
        else:
            img_array_copy[x,y] = 0

img_rgb = img.convert("RGB")
img_rgb_array = np.array(img_rgb)
# print(num)
# if num < 100:
#     print("图片过暗")
#     exit()


# 寻找下边界
lower_bound = []  # 存放下边界
lower_bound_x = []  # 存放下边界的x坐标
lower_bound_y = []  # 存放下边界的y坐标
for y in range(0, cols):
    for x in range(rows-1, 0, -1):
        v = img_array_copy[x, y]
        if v > 0:
            lower_bound.append([x, y])
            lower_bound_x.append(x)
            lower_bound_y.append(y)
            break
lower_bound_len = len(lower_bound)
# print(lower_bound_x)

# 拟合下边界
lower_bound_parameter = np.polyfit(lower_bound_y, lower_bound_x, 3)
# 存储拟合的下边界的坐标
y_lower_bound = []
try:
    for i in range(0, cols):
        y = int(lower_bound_parameter[0]*i**3 + lower_bound_parameter[1]*i**2 + lower_bound_parameter[2]*i +
                lower_bound_parameter[3])
        # img_rgb_array[y, i] = [0, 0, 255]
        y_lower_bound.append([y, i])
except IndexError as e:
    print("图片太暗，无法识别")


# 去除上半部不要的部分
img_array_2 = copy.copy(img_array)
for x in range(0, cols):
    for y in range(0, rows):
        if y <= y_lower_bound[x][0]:
            img_array_2[y, x] = 0
        else:
            break

for x in range(0,cols):
    for y in range(0,rows):
        if img_array_2[y, x] > 30:
            img_array_2[y,x] = 255
        else:
            img_array_2[y,x] = 0


img_final_array = copy.copy(img_array_2)

num = 0
for x in range(0,cols,20):
    for y in range(0,rows,20):
        num=0
        for a in range(0,20):
            for b in range(0,20):
                if img_final_array[y+b,x+a]>0:
                    num+=1
        if num<30:
            for a in range(0,20):
                for b in range(0,20):
                    img_final_array[y+b,x+a]=0


for x in range(0,cols,10):
    for y in range(0,rows,10):
        num=0
        for a in range(0,10):
            for b in range(0,10):
                if img_final_array[y+b,x+a]>0:
                    num+=1
        if num<10:
            for a in range(0,10):
                for b in range(0,10):
                    img_final_array[y+b,x+a]=0


img3 = Image.fromarray(img_final_array)
img4 = cv2.cvtColor(np.asarray(img3),cv2.COLOR_RGB2BGR)
cv2.namedWindow("input image",cv2.WINDOW_AUTOSIZE)
cv2.imshow("input image",img4)
lapalian_demo(img4)
cv2.waitKey()

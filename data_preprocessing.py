# 该代码用来数据预处理
import copy

from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

path = 'E:/LearningProjects/OCT脉络膜识别/HD/HDimage097.png'

img = Image.open(path)

rows = img.height  # 860
cols = img.width   # 500
num = 0

img_array = np.array(img)  # 把图片数组化
img_array_copy = copy.copy(img_array)
mylist = []  # 存储中间最亮的几行的坐标0

for x in range(0,rows):   # 如果灰度值大于210 就认为是中间的几行 可能存在误差，可以后期加上矫正算法
    for y in range(0,cols):
        v = img_array_copy[x,y]
        if v > 200:
            mylist.append([x,y])
            num = num+1
        else:
            img_array_copy[x,y] = 0

img_rgb = img.convert("RGB")
img_rgb_array = np.array(img_rgb)
print(num)
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
        img_rgb_array[y, i] = [0, 0, 255]
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

# img2 = Image.fromarray(img_array_2)
# img2.show()

for x in range(0,cols):
    for y in range(0,rows):
        if img_array_2[y, x] > 30:
            img_array_2[y,x] = 255
        else:
            img_array_2[y,x] = 0


img2 = Image.fromarray(img_array_2)
# img2.show()


# 腐蚀
img4 = cv2.cvtColor(np.asarray(img2),cv2.COLOR_RGB2BGR)
kernel = np.ones((2,2),dtype=np.uint8)
img_blur = cv2.erode(img4,kernel,2)

# cv2.imshow("img_blur",img_blur)
# cv2.waitKey()

img_final = Image.fromarray(cv2.cvtColor(img_blur,cv2.COLOR_BGR2GRAY))
img_final_array = np.array(img_final)

for x in range(0,cols):
    for y in range(0,rows):
        if y < y_lower_bound[x][0]+30 or y > y_lower_bound[x][0]+100:
            img_final_array[y,x] = 0
img3 = Image.fromarray(img_final_array)
img3.show()

# nihe_x = []
# nihe_y = []
# for x in range(0,cols):
#     for y in range(0,rows):
#         if img_final_array[y,x]>0:
#             nihe_x.append(x)
#             nihe_y.append(y)
#
# nihe_parameter = np.polyfit(nihe_x,nihe_y,4)
# for i in range(0,cols):
#     y = int(
#         nihe_parameter[0] * i ** 4 + nihe_parameter[1] * i ** 3 + nihe_parameter[2] * i ** 2 + nihe_parameter[3] * i +
#         nihe_parameter[4])
#     img_rgb_array[y, i] = [0,255,255]
# img3 = Image.fromarray(img_rgb_array)
# img3.show()
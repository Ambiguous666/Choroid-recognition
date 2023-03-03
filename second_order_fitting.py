from PIL import Image
import numpy as np
import cv2

path = 'E:/LearningProjects/OCT脉络膜识别/HD/HDimage097.png'  # 图97算是比较标准

img = Image.open(path)

rows = img.height  # 860
cols = img.width   # 500

img_array = np.array(img)  # 把图片数组化
mylist = []  # 存储中间最亮的几行的坐标

for x in range(0,rows):   # 如果灰度值大于220 就认为是中间的几行 可能存在误差，可以后期加上矫正算法
    for y in range(0,cols):
        v = img_array[x,y]
        if v > 60:                      # 标准是220
            mylist.append([x,y])
mylist_len = len(mylist)

# 将图中区域分块
different = int((mylist[mylist_len-1][0] - mylist[0][0])/4)
zone1 = mylist[0][0] + different
zone2 = zone1+different
zone3 = zone2 + different
zone4 = zone3 + different

# 将x，y的坐标分开
mylist_zone3_x = []
mylist_zone3_y = []

# 将第三块区域中的点存放在数组中
mylist_zone3 = []
for x in range(zone3,zone4):
    for y in range(0,cols):
        v = img_array[x,y]
        if v > 60:       # 一般设定为60
            mylist_zone3.append([x,y])
            mylist_zone3_x.append(x)
            mylist_zone3_y.append(y)

# print(mylist_zone3_x)
# print(mylist_zone3_y)

# 将灰度图像转换成RGB
img_rgb = img.convert("RGB")
img_rgb_array = np.array(img_rgb)

parameter = np.polyfit(mylist_zone3_y,mylist_zone3_x,2)
# y1 = parameter[0]*x**3 + parameter[1]*x**2 + parameter[2]*x + parameter[3]

# 绘制曲线
mylist_zone3_len = len(mylist_zone3)
for i in range(0,cols):
    y = int(parameter[0]*i**2 + parameter[1]*i + parameter[2])
    img_rgb_array[y,i] = [255,0,0]



# 框出不同的区域
# cv2.rectangle(img_rgb_array,(1,mylist[0][0]),(cols,zone1),(0,255,0),3)
# cv2.rectangle(img_rgb_array,(1,zone1),(cols,zone2),(255,0,0),3)
# cv2.rectangle(img_rgb_array,(1,zone2),(cols,zone3),(0,0,255),3)  # 真正要找的区域
# cv2.rectangle(img_rgb_array,(1,zone3),(cols,zone4),(0,255,255),3)

# 将最下面的区域涂成红色
mylist_zone3_len = len(mylist_zone3)
for i in range(0, mylist_zone3_len):
    x,y = mylist_zone3[i]
    img_rgb_array[x,y] = [255,0,0]



img2 = Image.fromarray(img_rgb_array)
img2.show()

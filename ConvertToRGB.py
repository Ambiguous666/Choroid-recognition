from PIL import Image
import numpy as np

path = 'E:/LearningProjects/OCT脉络膜识别/HD/HDimage055.png'

img = Image.open(path)
# img.show()

rows = img.height  # 860
cols = img.width   # 500

img_array = np.array(img)  # 把图片数组化
mylist = []  # 存储中间最亮的几行的坐标

for x in range(0,rows):   # 如果灰度值大于220 就认为是中间的几行 可能存在误差，可以后期加上矫正算法
    for y in range(0,cols):
        v = img_array[x,y]
        if v > 60:                      # 一般采用70
            mylist.append([x,y])
mylist_len = len(mylist)

img_rgb = img.convert("RGB")   # 将灰度图像转换成RGB
img_rgb_array = np.array(img_rgb)

for i in range(0,mylist_len):  # 将中间的区域涂成红色
    x,y = mylist[i]
    img_rgb_array[x,y] = [255,0,0]

img2 = Image.fromarray(img_rgb_array)
img2.show()


# print(mylist)




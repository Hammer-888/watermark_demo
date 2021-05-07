import numpy
import cv2

class IMG_LSB:

    def __init__(self, key=57):
        self.key = key
        self.ls_cover = None
        self.ls_info = None

    def create_cover(self, img_cover_name, img_info_name):
        """
        使用LSB算法对图像进行隐藏，隐藏到使用key作为种子生成的随机数指定的RGB通道中
        :param img_cover_name: 载体图片名
        :param img_info_name: 隐体图片名
        :param save_img_name: LSB生成后的图片保存位置以及名字
        :return: LSB生成后的图片矩阵
        """
        img_info = cv2.imread(img_info_name)
        img_cover =cv2.imread(img_cover_name)
        self.ls_info = img_info.shape[:2] # 得到隐体图片的长和宽
        self.ls_cover = img_cover.shape[:2] # 得到载体的长和宽
        # print(self.ls_info,self.ls_cover)
        if self.ls_info > self.ls_cover:
            print("载体太小")
        # 开始隐藏
        numpy.random.seed(self.key)
        for i in range(0, self.ls_info[0]):
            for j in range(0, self.ls_info[1]):
                if (img_info[i][j] == 255).any():  # 如果隐体为255则藏在R层最低为置为1
                    img_cover[i, j, numpy.random.randint(0, 3)] |= 1    # 随机选定一个通道进行隐藏
                else:
                    img_cover[i, j, numpy.random.randint(0, 3)] &= 254  # 如果隐体为0则藏在R层最低为置为0

        # cv2.imwrite(save_img_name, img_cover)
        return img_cover

    def  extract_img(self,img_info_name, blmb_name, save_img_name):
        """
        对隐体进行提取并显示
        :param blmb_name: LSB生成的含有隐体的载体名
        :param save_img_name: 提取后的隐体存储的位置
        :return: 提取后的隐体的矩阵
        """
        self.ls_info=cv2.imread(img_info_name).shape[:2]
        blmb = cv2.imread(blmb_name)
        matrix = [[255 for i in range(self.ls_info[0])] for i in range(self.ls_info[1])]    # 生成与隐体相同大小的矩阵，并赋值为255
        re_info_img = numpy.array(matrix, dtype=numpy.uint8).T   # 将生成的矩阵转化为可存储图像的8位格式
        # 开始提取
        numpy.random.seed(self.key)
        for i in range(0, self.ls_info[0]):
            for j in range(0, self.ls_info[1]):
                randint_value = numpy.random.randint(0, 3)  # 使用seed控制随机数的生成保证与之前隐藏时，生成的随机数一致
                blmb[i, j, randint_value] &= 1 # 取出最后一位
                if blmb[i, j, randint_value] == 0:
                    re_info_img[i][j] &= 0     # 如果最后一位为0则隐体原处为0，为1则为255
                else:
                    re_info_img[i][j] |= 255
        cv2.imwrite(save_img_name,re_info_img)
        return re_info_img



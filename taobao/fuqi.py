import cv2
import numpy
import os
import time

path = os.getcwd() + '\\'


class ImageElement(object):
    def __init__(self, imgPath, imgObj, imgW, imgH):
        # print("调用__init__方法")
        self.imgPath = imgPath
        self.imgObj = imgObj
        self.imgW = imgW
        self.imgH = imgH


img_dir = "click_img2"
no_img_dir = "no_img2"

# img_path1 = './' + img_dir + '/1.png'
# a_img1 = cv2.imread(img_path1, -1)  # 读取按钮图片
# a1, w1, h1 = a_img1.shape[::-1]  # a   ;w 图片宽度;h 图片高度
# print("图片1[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path1, a1, w1, h1))
# IMAGE1 = ImageElement(img_path1, a_img1, w1, h1)
# 
# img_path2 = './' + img_dir + '/2.png'
# a_img2 = cv2.imread(img_path2, -1)  # 读取按钮图片
# a2, w2, h2 = a_img2.shape[::-1]  # a   ;w 图片宽度;h 图片高度
# print("图片2[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path2, a2, w2, h2))
# IMAGE2 = ImageElement(img_path2, a_img2, w2, h2)
# 
# img_path3 = './' + img_dir + '/3.png'
# a_img3 = cv2.imread(img_path3, -1)  # 读取按钮图片
# a3, w3, h3 = a_img3.shape[::-1]  # a   ;w 图片宽度;h 图片高度
# print("图片3[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path3, a3, w3, h3))
# IMAGE3 = ImageElement(img_path3, a_img3, w3, h3)
# 
# no_img_path1 = './' + no_img_dir + '/1.png'
# no_img1 = cv2.imread(no_img_path1, -1)  # 读取按钮图片
# no_a1, no_w1, no_h1 = no_img1.shape[::-1]  # a   ;w 图片宽度;h 图片高度
# print("图片忽略1[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (no_img_path1, no_a1, no_w1, no_h1))
# print("      -----过滤图片1, no_img1=%s" % no_img1)
# 
# no_img_path2 = './' + no_img_dir + '/2.png'
# no_img2 = cv2.imread(no_img_path2, -1)  # 读取按钮图片
# no_a2, no_w2, no_h2 = no_img2.shape[::-1]  # a   ;w 图片宽度;h 图片高度
# print("图片忽略2[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (no_img_path2, no_a2, no_w2, no_h2))

match_percent = 0.85

ignore_data2 = []
click_data2 = []

# 存放文件路径的数组
clickImagesList = []
noImagesList = []

filepathList = []
nofilepathList = []


def list_dir_files(pathList, prepath, name, suffix):
    path = os.path.join(prepath, name)
    if os.path.isfile(path):
        print("  列举文件路径 path=[%s]" % (path))
        if path.endswith(suffix):
            pathList.append(path)
    elif os.path.isdir:
        ls = os.listdir(path)
        for item in ls:
            list_dir_files(pathList, path, item, suffix)


def find_my_click_images(fileslist):
    for filepath in fileslist:
        img_path = filepath
        img_obj = cv2.imread(img_path, -1)  # 读取按钮图片
        img_a, img_w, img_h = img_obj.shape[::-1]  # a   ;w 图片宽度;h 图片高度
        print("点击图片[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path, img_a, img_w, img_h))
        new_img = ImageElement(img_path, img_obj, img_w, img_h)
        clickImagesList.append(new_img)


def find_my_no_images(fileslist):
    for filepath in fileslist:
        img_path = filepath
        img_obj = cv2.imread(img_path, -1)  # 读取按钮图片
        img_a, img_w, img_h = img_obj.shape[::-1]  # a   ;w 图片宽度;h 图片高度
        print("忽略图片[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path, img_a, img_w, img_h))
        new_img = ImageElement(img_path, img_obj, img_w, img_h)
        noImagesList.append(new_img)


def click(x, y):
    print("!!!!!!!!!click 坐标=[%d, %d]" % (x, y))
    os.system("adb shell input tap %d %d" % (x, y))


def sweep(x0, y0, x1, y1, ctime=500):
    os.system("adb shell input touchscreen swipe %d %d %d %d %d" % (x0, y0, x1, y1, ctime))


def long_click(x, y, ctime=1000):
    sweep(x, y, x + 5, y + 5, ctime)


def if_is_no_images(current_data_pos_h):
    print("if_is_no_images, 判断图片y=[%d], 而忽略图片的坐标是{  %s  }---len=%d" % (current_data_pos_h, ignore_data2, len(ignore_data2)))
    idx = 0
    for i in range(0, len(ignore_data2)):
        # print("      ---i=%r " % (i))
        # print("      ---[%d]=%r " % (i, ignore_data2[i]))
        # print("      ---[%d][0]=%r " % (i, ignore_data2[i][0]))
        # print("      ---[%d][0][0]=%r " % (i, ignore_data2[i][0][0]))
        # print("      ---[%d][0][1]=%r " % (i, ignore_data2[i][0][1]))
        # print("      ---(%d+40) > %d > (%d-40) ??" % (ignore_data2[i][0][1], current_data_pos_h, ignore_data2[i][0][1]))
        if ignore_data2[i][0][1] + 40 > current_data_pos_h > ignore_data2[i][0][1] - 40:
            # print("  这个图片为过滤, x=[%d],y=[%d]" % (current_data[0], current_data[1]))
            print("  这个图片为过滤, y=[%d]" % (current_data_pos_h))
            return True
    return False


def match_img_single(img, click_img, ignore_data2, w, h):
    try:
        print("匹配点击图片, 开始 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print("matchTemplate begin")
        res = cv2.matchTemplate(img, click_img, cv2.TM_CCOEFF_NORMED)  # 在img图片中查找a_img
        # print("matchTemplate end")
        # print("打印坐标 begin")
        # print(res)
        # print("打印坐标 end")
        print("判断匹配度是否包含>=%.2f" % match_percent)
        loc = numpy.where(res >= match_percent)  # 匹配程度大于80%的坐标y,x
        data = []
        for pt in zip(*loc[::-1]):  # *号表示可选参数
            data.append(pt)
        # print("匹配数据打印 begin")
        # print(data)
        # print("匹配数据打印 end")
        print("匹配点击图片, 结束 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        data2 = []
        if data:
            data2.append([data[0][0] + w // 2, data[0][1] + h // 2])

        for i in range(1, len(data)):
            if ignore_data2:
                if if_is_no_images(data[i][1] + h // 2):
                    continue
            print("    ____data[%d], [i][0]=[%d],[i-1][0]=[%d], [i][1]=[%d],[i-1][1]=[%d]]" % (i, data[i][0], data[i - 1][0], data[i][1], data[i - 1][1]))
            if data[i][0] > data[i - 1][0] + 10 or data[i][0] < data[i - 1][0] - 10:
                if data[i][1] > data[i - 1][1] + 10 or data[i][1] < data[i - 1][1] - 10:
                    # data2.append(data[i])
                    data2.append([data[i][0] + w // 2, data[i][1] + h // 2])
                    print("    data2--1--加入新坐标 [%d, %d]" % (data[i][0] + w // 2, data[i][1] + h // 2))
                else:
                    # print("    data2--1--不加入坐标-- [%d, %d]" % (data[i][0] + w // 2, data[i][1] + h // 2))
                    # print("    data2--1--不加入坐标-- data[i][0]=[%d], data[i - 1][0] + 10=[%d]" % (data[i][0], data[i - 1][0] + 10))
                    pass
            elif data[i][1] > data[i - 1][1] + 10 or data[i][1] < data[i - 1][1] - 10:
                # data2.append(data[i])
                data2.append([data[i][0] + w // 2, data[i][1] + h // 2])
                print("    data2--2--新坐标加入 [%d, %d]" % (data[i][0] + w // 2, data[i][1] + h // 2))
            else:
                # print("    data2--3--不加入坐标-- [%d, %d]" % (data[i][0] + w // 2, data[i][1] + h // 2))
                # print("    data2--3--不加入坐标-- data[i][0]=[%d], data[i - 1][0] + 10=[%d]" % (data[i][0], data[i - 1][0] + 10))
                pass
    except Exception as e:
        print("匹配点击图片, 异常, return false, 错误为 str(%s)" % e)
        return False

    if data2:
        if if_is_no_images(data[0][1] + h // 2):
            data2.remove([data[0][0] + w // 2, data[0][1] + h // 2])
            print("    匹配点击图片, 移除第1个坐标-- [%d, %d]" % (data[0][0] + w // 2, data[0][1] + h // 2))

    if data2:
        print("匹配点击图片, 新增坐标{  %s  }" % data2)
        click_data2.append(data2)
    else:
        print("匹配点击图片, 无 新增坐标")

    return click_data2


def match_no_img(img, no_img, w, h):
    print("匹配过滤图片, 开始 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    try:
        # print("matchTemplate begin")
        # print("      -----匹配过滤图片, no_img=%s" % no_img1)
        no_res = cv2.matchTemplate(img, no_img, cv2.TM_CCOEFF_NORMED)  # 在img图片中查找a_img
        # print("matchTemplate end")
        # print("打印坐标 begin")
        # print(no_res)
        # print("打印坐标 end")
        # print("判断匹配度是否包含>=%.2f begin" % match_percent)
        no_loc = numpy.where(no_res >= match_percent)  # 匹配程度大于80%的坐标y,x
        # print("判断匹配度是否包含>=%.2f end" % match_percent)
        no_data = []
        for pt in zip(*no_loc[::-1]):  # *号表示可选参数
            no_data.append(pt)
        # print("匹配数据打印 begin")
        # print(no_data)
        # print("匹配数据打印 end")

        no_data2 = []
        if no_data:
            no_data2.append([no_data[0][0] + w // 2, no_data[0][1] + h // 2])
        # print("ignore_data2 第一条 begin")
        # print(ignore_data2)
        # print("ignore_data2 第一条 end")

        for i in range(1, len(no_data)):
            if no_data[i][0] > no_data[i - 1][0] + 10 or no_data[i][0] < no_data[i - 1][0] - 10:
                if no_data[i][1] > no_data[i - 1][1] + 10 or no_data[i][1] < no_data[i - 1][1] - 10:
                    # data2.append(no_data[i])
                    print("    no_data2--1--新坐标加入 [%d, %d]" % (no_data[i][0] + w // 2, no_data[i][1] + h // 2))
                    no_data2.append([no_data[i][0] + w // 2, no_data[i][1] + h // 2])
                else:
                    pass
            elif no_data[i][1] > no_data[i - 1][1] + 10 or no_data[i][1] < no_data[i - 1][1] - 10:
                # data2.append(no_data[i])
                print("    no_data2--2--新坐标加入 [%d,%d]" % (no_data[i][0] + w // 2, no_data[i][1] + h // 2))
                no_data2.append([no_data[i][0] + w // 2, no_data[i][1] + h // 2])
            else:
                pass
    except Exception as e:
        print("匹配过滤图片, 异常, return false, 错误为 str(%s)" % e)
        print(str(e))
        return False

    if no_data2:
        print("匹配过滤图片, 新增坐标{  %s  }" % no_data2)
        ignore_data2.append(no_data2)
    else:
        print("匹配过滤图片, 无 新增坐标")

    print("匹配过滤图片, 结束 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    return ignore_data2


def do_screencap():
    os.system('adb shell screencap -p /sdcard/screencap.png')
    os.system('adb pull /sdcard/screencap.png ' + path + 'screencap.png')


def match_img():
    print('截图...')
    do_screencap()
    screencap_img = cv2.imread('screencap.png', -1)  # 读取图片

    print("")
    print('检测过滤图片按钮...')
    # ignore_data2 = []
    del ignore_data2[:]
    # print('noImagesList》》》》》》》》》》》》》》》》')
    # print(noImagesList)
    # print('noImagesList<<<<<<<<<<<<<<<<<<<<<<')
    for i in range(0, len(noImagesList)):
        print(' 当前过滤图片... %s' % noImagesList[i].imgPath)
        img_element = noImagesList[i]
        match_no_img(screencap_img, img_element.imgObj, img_element.imgW, img_element.imgH)
        # print(' 当前过滤图片... %s 坐标打印开始>>>>>>>>>>>>>>>>' % noImagesList[i].imgPath)
        # print(ignore_data2)
        # print(' 当前过滤图片... %s 坐标打印结束<<<<<<<<<<<<<<<<' % noImagesList[i].imgPath)

    if ignore_data2:
        print("匹配过滤图片, 最终的坐标{  %s  }" % ignore_data2)
    else:
        print("匹配过滤图片, 最终的坐标 为 空")

    print("")
    print("")
    print('检测点击图片按钮...')
    idx = 0
    del click_data2[:]
    for i in range(0, len(clickImagesList)):
        img_element = clickImagesList[i]
        idx = idx+1
        print('检测到到第%d个点击图片按钮' % idx)
        match_img_single(screencap_img, img_element.imgObj, ignore_data2, img_element.imgW, img_element.imgH)

    if click_data2:
        print("匹配点击图片, 最终的坐标{  %s  }" % click_data2)
    else:
        print("匹配点击图片, 最终的坐标 为 空")
    #
    # data3 = match_img_single(screencap_img, a_img1, ignore_data2, w1, h1)
    # if data3:
    #     print('检测到到第1个点击图片按钮')
    #     return data3
    # else:
    #     print('检测第2个点击图片按钮...')
    #     data3 = match_img_single(screencap_img, a_img2, ignore_data2, w2, h2)
    #     if data3:
    #         print('检测到到第2个点击图片按钮')
    #         return data3
    #     else:
    #         print('检测第3个点击图片按钮...')
    #         data3 = match_img_single(screencap_img, a_img3, ignore_data2, w3, h3)
    #         if data3:
    #             print('检测到到第3个点击图片按钮')
    #             return data3
    #         else:
    #             pass


def op1_just_sleep():
    time.sleep(15)
    # sweep(550, 500, 550, 600, 15000)  # 滑动5秒
    time.sleep(5)
    # sweep(550, 1600, 550, 600, 5000)
    # sweep(550, 1600, 550, 600, 5000)
    # sweep(550, 1600, 550, 600, 5000)


def click_back_key():
    os.system('adb shell input keyevent 4 ')  # 点击返回

image_parent_dir = "."
click_image_dir_name = 'click_img'
ignore_image_dir_name = 'no_img'

def main():
    print("查找需要点击按钮图标列表, begin")
    list_dir_files(filepathList, image_parent_dir, click_image_dir_name, ".png")
    print("查找需要点击按钮图标列表, 打印列表")
    print("   %r " % filepathList)
    print("查找需要点击按钮图标列表, 打印列表结束")
    find_my_click_images(filepathList)
    print("")

    print("查找需要忽略图标列表-----begin")
    list_dir_files(nofilepathList, image_parent_dir, ignore_image_dir_name, ".png")
    print("查找需要忽略图标列表, 打印列表")
    print("   %r " % nofilepathList)
    print("查找需要忽略图标列表, 打印列表结束")
    find_my_no_images(nofilepathList)

    print("")
    print("开始自动运行脚本")

    while True:
        match_img()
        lists = click_data2
        print("match_img return lists begin")
        print(lists)
        print("match_img return lists end")

        # if lists:
        #     print('测试，直接返回！')
        #     return

        if lists:
            click(lists[0][0][0], lists[0][0][1])
            op1_just_sleep()
            click_back_key()
            time.sleep(3)
        else:
            ##os.system('adb shell input keyevent 4 ')    # 点击返回
            ##time.sleep(3)
            ##if match_img():
            ##    pass
            ##else:
            print('Error！请回到活动页面！')
            break


if __name__ == '__main__':
    main()

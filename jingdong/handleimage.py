import cv2
import numpy
import os
import time
import command

# ignore_images_pos = []
# click_images_pos = []

# 存放文件路径的数组
# click_images_path_list = []
# no_images_path_list = []

# file_path_list = []
# no_file_path_list = []

# 图片识别匹配百分比
MATCH_PERCENT = 0.85

# 当前目录，用于保存截屏图片
local_save_dir = os.getcwd() + '\\'
# 截屏图片名称
SCREEN_CAP_IMAGE_NAME = 'screencap.png'


# 将图片object转换为ImageElement对象
class ImageElement(object):
    def __init__(self, img_path, img_obj, img_w, img_h):
        # print("调用__init__方法")
        self.imgPath = img_path
        self.imgObj = img_obj
        self.imgW = img_w
        self.imgH = img_h


# 从整张截图中抠取小点击图片（排除忽略图片），并返回其坐标
def match_img_single(whole_img, click_img, ignore_img_pos_list, w, h, is_ignore):
    # 将要返回的坐标数组
    img_pos_list = []
    if is_ignore is True:
        cur_img_type = '忽略图片'
    else:
        cur_img_type = '点击图片'

    try:
        print("匹配" + cur_img_type + ", 开始 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print("matchTemplate begin")
        # 在 whole_img 图片中查找 click_img
        res = cv2.matchTemplate(whole_img, click_img, cv2.TM_CCOEFF_NORMED)
        # print("matchTemplate end")
        # print("打印坐标 begin")
        # print(res)
        # print("打印坐标 end")
        print("判断匹配度是否包含>=%.2f" % MATCH_PERCENT)
        loc = numpy.where(res >= MATCH_PERCENT)  # 匹配程度大于80%的坐标y,x
        # data 保存小图识别出来的所有坐标
        data = []
        for pt in zip(*loc[::-1]):  # *号表示可选参数
            data.append(pt)
        # print("匹配数据打印 begin")
        # print(data)
        # print("匹配数据打印 end")
        print("匹配" + cur_img_type + ", 结束 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # data2 保存后面使用的图片坐标
        data2 = []
        # 总是把首个坐标加入到 data2 中
        if data:
            data2.append([data[0][0] + w // 2, data[0][1] + h // 2])

        # 遍历 data ， 加入到 data2 中， 需要移除相近的坐标（其实是同一个图片）
        for i in range(1, len(data)):
            # 判断当前图片坐标是否是忽略图片的坐标
            if is_ignore is False:
                if ignore_img_pos_list:
                    if is_ignore_images(data[i][1] + h // 2, ignore_img_pos_list):
                        continue
            print("    ____data[%d], [i][0]=[%d],[i-1][0]=[%d], [i][1]=[%d],[i-1][1]=[%d]]" % (
                i, data[i][0], data[i - 1][0], data[i][1], data[i - 1][1]))
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
        print("匹配" + cur_img_type + ", 异常, return false, 错误为 str(%s)" % e)
        return False

    if data2:
        if is_ignore is False:
            # 二次判断，移除忽略图片
            if is_ignore_images(data[0][1] + h // 2, ignore_img_pos_list):
                data2.remove([data[0][0] + w // 2, data[0][1] + h // 2])
                print("    匹配" + cur_img_type + ", 移除第1个坐标-- [%d, %d]" % (data[0][0] + w // 2, data[0][1] + h // 2))

    if data2:
        print("匹配" + cur_img_type + ", 新增坐标{  %s  }" % data2)
        img_pos_list.append(data2)
    else:
        print("匹配" + cur_img_type + ", 无 新增坐标")

    return img_pos_list


# 判断指定图片纵坐标，是否与忽略图片坐标相近，相近则表示它属于忽略图片
# cur_img_pos_y 图片的纵坐标
# ignore_img_pos_list 忽略图片列表坐标集合
def is_ignore_images(cur_img_pos_y, ignore_img_pos_list):
    print("is_ignore_images, 判断图片y=[%d], 而忽略图片的坐标是{  %s  }, len=[%d]" % (
        cur_img_pos_y, ignore_img_pos_list, len(ignore_img_pos_list)))
    OFFSET = 40
    # print("开始判断坐标, y=[%d]" % cur_img_pos_y)
    # print("开始判断坐标, [0][0]=[%r]" % ignore_img_pos_list[0][0])
    # print("开始判断坐标, [0][0][0]=[%r]" % ignore_img_pos_list[0][0][0])
    # print("开始判断坐标, [0][0][0][0]=[%r]" % ignore_img_pos_list[0][0][0][0])
    # print("开始判断坐标, [0][0][0][0][0]=[%s]" % ignore_img_pos_list[0][0][0][0][0])
    # aaaa = ignore_img_pos_list[0][0][1] + OFFSET
    # print("开始判断坐标, aaaa=[%d]" % aaaa)
    #is_ignore_images, 判断图片y=[696], 而忽略图片的坐标是{  [[[[137, 695]]], [[[139, 1469]]], [[[303, 1633]]]]  }, len=[3]
      # ---i=0
      # ---[0]=[[[137, 695]]]
      # ---[0][0]=[[137, 695]]
      # ---[0][0][0]=[137, 695]
      # ---[0][0][0][1]=695
    for i in range(0, len(ignore_img_pos_list)):
        print("      ---i=%r " % (i))
        print("      ---[%d]=%r " % (i, ignore_img_pos_list[i]))
        print("      ---[%d][0]=%r " % (i, ignore_img_pos_list[i][0]))
        print("      ---[%d][0][0]=%r " % (i, ignore_img_pos_list[i][0][0]))
        print("      ---[%d][0][0][1]=%r " % (i, ignore_img_pos_list[i][0][0][1]))
        print("      ---(%d+40) > %d > (%d-40) ??" % (ignore_img_pos_list[i][0][0][1], cur_img_pos_y, ignore_img_pos_list[i][0][0][1]))
        # 当前图片的y坐标 与 忽略图片列表中每个图片的y坐标 比较，如果在 -OFFSET~OFFSET 范围内，则认为它也是忽略图片
        if ignore_img_pos_list[i][0][0][1] + OFFSET > cur_img_pos_y > ignore_img_pos_list[i][0][0][1] - OFFSET:
            # print("  这个图片为过滤, x=[%d],y=[%d]" % (current_data[0], current_data[1]))
            print("  这个图片为过滤图片, y=[%d]" % cur_img_pos_y)
            return True
        else:
            print("  这个图片为不是过滤图片, y=[%d]" % cur_img_pos_y)
    return False


# 找到可点击按钮的坐标数据，排除忽略按钮
def match_img(click_img_list, ignore_img_list):
    print('截图...')
    command.do_screen_cap(local_save_dir, SCREEN_CAP_IMAGE_NAME)
    # 用cv2库解析截屏图片
    screen_cap_img = cv2.imread(SCREEN_CAP_IMAGE_NAME, -1)

    print("")

    # 先识别过滤图片，并得到其坐标，保存到数组 ignore_img_pos_list
    ignore_img_pos_list = []
    print('检测过滤图片按钮...')
    for i in range(0, len(ignore_img_list)):
        print(' 当前过滤图片... %s' % ignore_img_list[i].imgPath)
        img_element = ignore_img_list[i]
        img_pos_list = match_img_single(screen_cap_img,
                                               img_element.imgObj,
                                               None,
                                               img_element.imgW,
                                               img_element.imgH,
                                               True)
        if img_pos_list:
            ignore_img_pos_list.append(img_pos_list)

    if ignore_img_pos_list:
        print("匹配过滤图片, 最终的坐标{  %s  }" % ignore_img_pos_list)
    else:
        print("匹配过滤图片, 最终的坐标 为 空")

    print("")
    print("")

    # 先识别点击按钮图片，并得到其坐标，保存到数组 click_img_pos_list
    click_img_pos_list = []
    print('检测点击图片按钮...')
    idx = 0
    for i in range(0, len(click_img_list)):
        img_element = click_img_list[i]
        idx = idx + 1
        print('检测到到第%d个点击图片按钮' % idx)
        img_pos_list = match_img_single(screen_cap_img,
                                              img_element.imgObj,
                                              ignore_img_pos_list,
                                              img_element.imgW,
                                              img_element.imgH,
                                              False)
        if img_pos_list:
            click_img_pos_list.append(img_pos_list)

    if click_img_pos_list:
        print("匹配点击图片, 最终的坐标{  %s  }" % click_img_pos_list)
    else:
        print("匹配点击图片, 最终的坐标 为 空")

    # 得到最终图片坐标数组
    return click_img_pos_list


# 遍历指定目录中的指定后缀的图片文件，并保存到参数 path_list 中
def list_dir_files(path_list, parent_dir, dir_name, file_suffix):
    cur_path = os.path.join(parent_dir, dir_name)
    if os.path.isfile(cur_path):
        print("  列举文件路径 path=[%s]" % cur_path)
        if cur_path.endswith(file_suffix):
            path_list.append(cur_path)
    elif os.path.isdir:
        ls = os.listdir(cur_path)
        for item in ls:
            list_dir_files(path_list, cur_path, item, file_suffix)


# 读取文件路径列表，最终返回 ImageElement 类型的数组
def find_my_images(files_path_list):
    # 保存到数组 local_img_list
    local_img_list = []
    for file_path in files_path_list:
        img_path = file_path
        img_obj = cv2.imread(img_path, -1)  # 读取按钮图片
        img_a, img_w, img_h = img_obj.shape[::-1]  # a   ;w 图片宽度;h 图片高度
        print("遍历本地匹配图片[%s] 通道数a=%d, 宽w=%d, 高h=%d" % (img_path, img_a, img_w, img_h))
        new_img = ImageElement(img_path, img_obj, img_w, img_h)
        local_img_list.append(new_img)
    return local_img_list

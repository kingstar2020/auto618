import sys

import cv2
import numpy
import os
import time
import handleimage
import command

path = os.getcwd() + '\\'

image_parent_dir = "."
click_image_dir_name = 'click_img'
ignore_image_dir_name = 'no_img'
pic_ext_name = '.png'
click_image2_dir_name = 'click_img2'


# 操作累心1， 仅等待
def op1_just_sleep():
    time.sleep(15)
    # sweep(550, 500, 550, 600, 15000)  # 滑动5秒
    time.sleep(15)
    # sweep(550, 1600, 550, 600, 5000)
    # sweep(550, 1600, 550, 600, 5000)
    # sweep(550, 1600, 550, 600, 5000)


def main():
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    arg_cnt = len(sys.argv)

    sn = ''
    if arg_cnt > 1:
        sn = sys.argv[1]

    print('sn:', sn)

    # command.set_device_sn('192.168.50.150:5555')
    # command.set_device_sn('UJN0221227001889')
    command.set_device_sn(sn)
    
    print("查找需要点击按钮图标列表, begin")
    file_path_list = []
    handleimage.list_dir_files(file_path_list, image_parent_dir, click_image_dir_name, pic_ext_name)
    print("查找需要点击按钮图标列表, 打印列表")
    print("   %r " % file_path_list)
    print("查找需要点击按钮图标列表, 打印列表结束")
    click_images_list = handleimage.find_my_images(file_path_list)
    print("")

    print("查找需要点击按钮图标2列表, begin")
    file_path_list2 = []
    handleimage.list_dir_files(file_path_list2, image_parent_dir, click_image2_dir_name, pic_ext_name)
    print("查找需要点击按钮图标2列表, 打印列表")
    print("   %r " % file_path_list2)
    print("查找需要点击按钮图标2列表, 打印列表结束")
    click_images_list2 = handleimage.find_my_images(file_path_list2)
    print("")

    print("查找需要忽略图标列表-----begin")
    no_file_path_list = []
    handleimage.list_dir_files(no_file_path_list, image_parent_dir, ignore_image_dir_name, pic_ext_name)
    print("查找需要忽略图标列表, 打印列表")
    print("   %r " % no_file_path_list)
    print("查找需要忽略图标列表, 打印列表结束")
    ignore_images_list = handleimage.find_my_images(no_file_path_list)

    print("")
    print("开始自动运行脚本")

    while True:
        # 识别出最终要点击的坐标
        lists = handleimage.match_img(click_images_list, ignore_images_list)
        print("match_img return lists begin")
        print(lists)
        print("match_img return lists end")

        if lists:
            # 执行点击动作
            command.click(lists[0][0][0][0], lists[0][0][0][1])

            # 执行操作类型1
            op1_just_sleep()

            # 执行点击返回操作
            command.click_back_key()

            # 等待网络和页面刷新一段时间后，继续循环
            time.sleep(1)

            # 支付宝
            # 匹配开心手下按钮，并点击，最后再循环
            # lists = handleimage.match_img(click_images_list2, ignore_images_list)
            # print("match_img 二次 return lists begin")
            # print(lists)
            # print("match_img 二次 return lists end")
            # if lists:
            #     # 执行点击动作
            #     command.click(lists[0][0][0][0], lists[0][0][0][1])
            #     # 等待网络和页面刷新一段时间后，继续循环
            #     time.sleep(3)
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

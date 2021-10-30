import os

# DEVICE_SN = '192.168.50.150:5555'
DEVICE_SN = ''


# 对 DEVICE_SN 重新赋值
def set_device_sn(sn):
    global DEVICE_SN
    DEVICE_SN = sn
    print('set_device_sn=[%s]' % DEVICE_SN)


# adb截屏,并pull出图片到指定目录
def do_screen_cap(local_save_dir, screen_cap_image_name):
    if DEVICE_SN:
        os.system('adb -s ' + DEVICE_SN + ' shell screencap -p /sdcard/' + screen_cap_image_name)
        os.system(
            'adb -s ' + DEVICE_SN + ' pull /sdcard/' + screen_cap_image_name + ' ' + local_save_dir + screen_cap_image_name)
    else:
        os.system('adb shell screencap -p /sdcard/' + screen_cap_image_name)
        os.system('adb pull /sdcard/' + screen_cap_image_name + ' ' + local_save_dir + screen_cap_image_name)


# adb模拟后退键
def click_back_key():
    if DEVICE_SN:
        os.system('adb -s ' + DEVICE_SN + ' shell input keyevent 4 ')  # 点击返回
    else:
        os.system('adb shell input keyevent 4 ')  # 点击返回


# adb模拟点击动作
def click(x, y):
    print('!!!!!!!!!click 坐标=[%d, %d]' % (x, y))
    if DEVICE_SN:
        os.system('adb -s ' + DEVICE_SN + ' shell input tap %d %d' % (x, y))
    else:
        os.system('adb shell input tap %d %d' % (x, y))


# adb模拟滑动动作
def sweep(x0, y0, x1, y1, ctime=500):
    if DEVICE_SN:
        os.system('adb -s ' + DEVICE_SN + ' shell input touchscreen swipe %d %d %d %d %d' % (x0, y0, x1, y1, ctime))
    else:
        os.system('adb shell input touchscreen swipe %d %d %d %d %d' % (x0, y0, x1, y1, ctime))


# adb模拟长按动作
def long_click(x, y, ctime=1000):
    sweep(x, y, x + 5, y + 5, ctime)

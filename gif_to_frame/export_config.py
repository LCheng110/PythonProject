# coding=utf-8
import json
import os
from PIL import Image, ImageSequence
from collections import OrderedDict
import zipfile
import sys
import shutil

frameCount = 0
kerneframe = 0

# 获取gif每帧的速率
def getGifFrameRate():
    imageinfo = image.info
    if not imageinfo.has_key("duration"):
        print "gif不可用"
        exit(1)
    print image.info["duration"]
    return image.info["duration"]


# gif转成每一帧图片保存
def gifToImages(imageName):
    if not os.path.exists(imageName):
        os.mkdir(imageName)
    frames = [f.copy() for f in ImageSequence.Iterator(image)]
    i = 0
    for frame in frames:
        print frame
        frame.save(os.path.join(imageName, "gif" + str(i) + ".png"), "PNG")
        i += 1
    return i


# 生成 TimeArry list
def generateTimeArry(rate, num):
    array = []
    i = 0
    while i < num:
        frame = OrderedDict()
        frame["time"] = round(rate * i, 3)
        frame["pic"] = i
        array.append(frame)
        i += 1
    return array


# 把整个文件夹内的文件打包
def dirToZip():
    f = zipfile.ZipFile(gifPath + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(gifPath):
        print dirpath
        for filename in filenames:
            f.write(os.path.join(dirpath, filename), filename)
    f.close()


print os.getcwd()
# gifPath = raw_input("输入gif文件名称：")
# pid = raw_input("输入pid：")
gifPath = sys.argv[1]
pid = sys.argv[2]
# gifPath = os.path.join("Downloads", gifPath)
gifName = os.path.split(gifPath)[1]
n = "gif"
pid = int(pid)

image = Image.open(gifPath + ".gif")
imageSize = image.size
c = gifToImages(gifPath)
rate = round(float(getGifFrameRate()) / 1000, 3)
du = round(rate * c, 3)
print du
print c
print rate

config = OrderedDict(
    [("pid", pid), ("fid", 2), ("du", du), ("type", 2), ("x", 320.0), ("y", 640.0), ("w", imageSize[0]), ("h", imageSize[1]),
     ("a", 0.0), ("fx", 0), ("fy", 0), ("fw", 0), ("fh", 0), ("n", str(n)), ("c", c),
     ("kerneframe", kerneframe), ("pExtend", 1), ("extendSection", 0), ("frameArry", generateTimeArry(rate, c))])
timeArray = []
timeOption = OrderedDict(
    [('beginTime', 0.0), ('endTime', round(du, 2)), ('shrink', 1), ('minTime', round(du, 2)), ('maxTime', 0)])
timeArray.append(timeOption)
config["timeArry"] = timeArray
with open(os.path.join(gifPath, "config.json"), "w") as file :
    file.write(json.dumps(config, indent=4))
dirToZip()
image.close()
# shutil.rmtree(gifPath)

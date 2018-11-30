# coding: utf-8

import os
import re
import time

# 前缀
PREFIXNAME = "PY_"
# 图片路径(绝对路径)
IMAGEPATH = "/Users/***/Desktop/项目名称/Assets.xcassets"
# 文件路径(绝对路径)
FILEPATH = "/Users/***/Desktop/项目名称"


# 图片文件名称后缀
IMAGEFILEEND = ".imageset"
# 图片名称后缀
IMGAENAMEEND = ".png"

#--------------------------------修改项目图片名称------------------------------------------#

# 修改项目图片名称
def changeProgectImageName():
    getImageName(IMAGEPATH)
    scanFilesContent(FILEPATH)

# 修改名称规则
def changeNameRule(oldName):
    # return PREFIXNAME + oldName
    return oldName[2:]

# 获取所有图片名称
def getImageName(path):
    if not os.path.exists(path):
        print("文件不存在" + path)
        return
    fileList = os.listdir(path)
    for file in fileList:
        if file.startswith("."):
            continue
        currentPath = os.path.join('%s/%s' % (path, file))
        if currentPath.endswith(IMAGEFILEEND):
            imageNameList.append(file[:-len(IMAGEFILEEND)])
            currentPath = changeFilePathName(currentPath)
            changeImageName(currentPath)
        if os.path.isfile(currentPath):
            continue
        getImageName(currentPath)

# 修改文件名称
def changeFilePathName(oldPath):
    if not os.path.exists(oldPath):
        print("文件不存在" + oldPath)
        return oldPath
    pathPuple =  os.path.split(oldPath)
    newName = changeNameRule(pathPuple[1])
    newPath = pathPuple[0] + "/" + newName
    os.rename(oldPath, newPath)
    print(oldPath)
    print(newPath)
    return newPath

# 修改图片名称
def changeImageName(path):
    if not os.path.exists(path):
        print("文件不存在" + path)
        return
    fileList = os.listdir(path)
    imageList = []
    for floder in fileList:
        if floder.endswith(IMGAENAMEEND):
            imageList.append(floder)
    for item in imageList:
        changeFilePathName(path + "/" + item)
        replaceFileContent(path + "/Contents.json", [item])

# 替换文件内容
def replaceFileContent(path, contentList, isOCStr = bool(0)):
    fileOpen = open(path)
    w_str = ""
    for line in fileOpen:
        w_str += replaceLineContent(contentList, line, isOCStr)
    writeOpen = open(path, 'w')
    writeOpen.write(w_str)
    fileOpen.close()
    writeOpen.close()

# 替换行中内容
def replaceLineContent(contentList, line, isOCStr = bool(0)):
    for item in contentList:
        oldName = item
        newName = changeNameRule(item)
        if isOCStr:
            oldName = "@\"" + oldName + "\""
            newName = "@\"" + newName + "\""
        if re.search(oldName, line):
            line = re.sub(oldName, newName, line)
    print(line)
    return line

# 扫描文件内容
def scanFilesContent(path):
    if not os.path.exists(path):
        print("文件不存在" + path)
        return
    fileList = os.listdir(path)
    for file in fileList:
        if file.startswith("."):
            continue
        currentPath = os.path.join('%s/%s' % (path, file))
        if currentPath.endswith(".m"):
            replaceFileContent(currentPath, imageNameList, bool(1))
        if os.path.isfile(currentPath):
            continue
        scanFilesContent(currentPath)


if __name__ == "__main__":
    start = time.process_time()
    # 修改项目图片名称
    imageNameList = []
    changeProgectImageName()

    end = time.process_time()
    print('Running time: %s Seconds' % (end - start))



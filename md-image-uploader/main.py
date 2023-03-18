# coding=utf-8
import sys
import os
import re
import minioUploader
import imagePathReplace
import pyperclip

def deformat(current_path, content, client, label):
    newContent = re.sub(r'\${2}((.|\n)*?)\${2}',r'```mathjax\1```', content)
    newContent = re.sub(r'\$(.+?)\$',r'`$\1$`', newContent)
    return imagePathReplace.replaceImagePath(current_path, newContent, client, label)
    

'''
+ 替换公式
+ 上传本地图片 + 替换
'''

if __name__ == '__main__':
    currentpath = sys.argv[0]
    filepath = sys.argv[1]
    if not filepath.endswith('md'):
        print('文件类型不支持')
        exit()
    filename = os.path.split(filepath)[-1]
    content = open(filepath, encoding='utf-8').read()
    dir_path = os.path.split(filepath)[0]
    current_dirpath = os.path.split(currentpath)[0]
    print(os.path.join(current_dirpath, "config.ini"))
    client = minioUploader.loadMinioClient(os.path.join(current_dirpath, "config.ini"))
    content = deformat(dir_path, content, client, filename)
    pyperclip.copy(content)

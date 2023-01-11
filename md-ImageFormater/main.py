# coding=utf-8
import requests
import shutil
import re
import os

pattern = re.compile(r'(!\[.*\]\((.*?)( +"(.*?)")?\))')

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def saveFile(url, filepath):
    r = requests.get(url) 
    if r.status_code == 200:
        with open(filepath, "wb") as code: code.write(r.content)
        return True
    else:
        return False



def saveImage(url, imageDir):
    mkdir(imageDir)
    imageName = os.path.split(url)[-1]
    p = imageName.find('?')
    if p != -1:
        imageName = imageName[:p]
    
    if url.startswith(("http", "https")):
        return saveFile(url, os.path.join(imageDir, imageName))
    elif os.path.isfile(url):
        shutil.copyfile(url, os.path.join(imageDir, imageName))
    else:
        print("unknown url: {}".format(url))    
    return True


def replace_path(m):
    filename = os.path.split(m.group(2))[-1]
    p = filename.find('?')
    if p != -1:
        filename = filename[:p]
    return m.group().replace(m.group(2), os.path.join("./assets", filename))

def collect(file_name, path, base):
    file_path = os.path.join(path, file_name)
    content = open(file_path, encoding='utf-8').read()
    for target in pattern.findall(content):
        url = target[1]
        saveImage(url, os.path.join(base, path, "assets"))
    newContent = pattern.sub(replace_path, content)

    newFilePath = os.path.join(base, path, file_name)
    with open(newFilePath, mode = "w", encoding='utf-8') as note: note.write(newContent)


def split_dir(current_path):
    file_list = []
    dir_list = []
    for sub in os.listdir(current_path):
        next_path = os.path.join(current_path, sub)
        if os.path.isdir(next_path):
            dir_list.append(sub)
        else:
            file_list.append(sub)
    return dir_list, file_list

def walk(current_path, output_path, depth):
    shift = depth * "    "
    mkdir(os.path.join(output_path, current_path))
    dir_list, file_list = split_dir(current_path)
    for filename in file_list:
        if filename.endswith("md"):
            print(shift + "dealing with: " + filename)
            collect(filename, current_path, output_path)
        else:
            shutil.copyfile(os.path.join(current_path, filename), os.path.join(output_path, current_path, filename))
    for dirname in dir_list:
        print(shift + "in: %s" % dirname)
        walk(os.path.join(current_path, dirname), output_path, depth + 1)
        print(shift + "out: %s" % dirname)


if __name__ == '__main__':
    current_path = "."
    output_path = current_path + "/../output"
    walk(current_path, output_path, 0)
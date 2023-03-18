# coding=utf-8
import sys
import requests
import shutil
import re
import os

pattern = re.compile(r'([!,\%]\[.*\]\((.*?)( +"(.*?)")?\))')

debug_mode : bool = False

def log(msg, depth = 0):
    shift = depth * "    "
    if debug_mode:
        print(shift + msg)

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

def parse_url(url):
    args = url.split('?')
    if len(args) < 2:
        return args[0], {}
    host = args[0]
    args = args[1].split('&')
    return host, dict(map(lambda item: item.split('='), args))

def mkdir_ignore_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_from_url_to_file(url, filepath):
    r = requests.get(url) 
    if r.status_code == 200:
        with open(filepath, "wb") as code: code.write(r.content)
        return True
    else:
        return False

def download_image_from_url_to_dir(url, image_output_dir, image_input_dir):
    image_path, args = parse_url(url)
    image_name = os.path.split(image_path)[-1]
    
    if url.startswith(("http", "https")):
        return download_from_url_to_file(url, os.path.join(image_output_dir, image_name))
    if not os.path.isabs(image_path):
        image_path = os.path.join(image_input_dir, image_path)
    
    if os.path.isfile(image_path):
        shutil.copyfile(image_path, os.path.join(image_output_dir, image_name))
    else:
        print("unknown url: {}".format(url))    
    return True


def replace_image_urls(re_machine):
    url = re_machine.group(2)
    image_path, args = parse_url(url)
    image_name = os.path.split(image_path)[-1]
    return re_machine.group().replace(re_machine.group(2), os.path.join("./assets", image_name))

def process_markdown_file(input_filepath, input_path, output_path):
    output_filepath = os.path.join(output_path, os.path.relpath(input_filepath, input_path))
    content = open(input_filepath, encoding='utf-8').read()
    image_output_dir = os.path.join(os.path.split(output_filepath)[0], "assets")
    image_input_dir = os.path.split(input_filepath)[0]
    mkdir_ignore_exist(image_output_dir)
    
    for target in pattern.findall(content):
        url = target[1]
        if not download_image_from_url_to_dir(url, image_output_dir, image_input_dir):
            log("can not download {}".format(url))
    new_content = pattern.sub(replace_image_urls, content)

    with open(output_filepath, mode = "w", encoding='utf-8') as text: text.write(new_content)

def walk_impl(current_path, input_path, output_path, depth):
    output_dir = os.path.join(output_path, os.path.relpath(current_path, input_path))
    mkdir_ignore_exist(output_dir)
    
    dirnames, filenames = split_dir(current_path)
    for filename in filenames:
        if filename.endswith(".md"):
            log("dealing with: {}".format(filename), depth)
            process_markdown_file(os.path.join(current_path, filename), input_path, output_path)
        else:
            shutil.copyfile(os.path.join(current_path, filename), os.path.join(output_dir, filename))
    
    for dirname in dirnames:
        log("in: {}".format(dirname), depth)
        walk_impl(os.path.join(current_path, dirname), input_path, output_path, depth + 1)
        log("out: {}".format(dirname), depth)

def walk(input_path, output_path):
    return walk_impl(input_path, input_path, output_path, 1)

if __name__ == '__main__':
    need_help = False
    input_path = "."
    output_path = "../output"
    args = sys.argv[1:]

    if len(args) >= 1 and not args[0].startswith("--"):
        input_path = args[0]
        args = args[1:]
    
    if len(args) >= 1 and not args[0].startswith("--"):
        output_path = args[0]
        args = args[1:]
    
    for arg in args:
        if arg.startswith("--"):
            if arg == "--debug":
                debug_mode = True
            elif arg == "--help":
                need_help = True
            else:
                print("unknown: {}".format(arg))
                state = 0
    if need_help:
        print("{} [input path] [output path] [--debug] [--help]".format(sys.argv[0]))
        print("default: input path = {}, output path = {}\n".format(input_path, output_path))

    log("input path = {}".format(input_path))
    log("output path = {}".format(output_path))

    if os.path.exists(output_path):
        print("output path: {}, exists!".format(output_path))
        exit(-1)
    
    walk(input_path, output_path)
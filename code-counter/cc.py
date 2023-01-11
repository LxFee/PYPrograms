"""
代码统计
"""
import os
import sys

filter_list : list = []
debug : bool = False

def log(msg, depth):
    shift = depth * "    "
    if debug:
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

def count(filepath):
    count = 0
    f = open(filepath, "r", encoding='UTF-8')
    for idx, line in enumerate(f):
        if len(line) > 1:
            count += 1
    return count


def walk(current_path, depth):
    total_line_num = 0
    try:
        dir_list, file_list = split_dir(current_path)
        for filename in file_list:
            ext = os.path.splitext(filename)[-1]
            if ext in filter_list:
                line_num = count(os.path.join(current_path, filename))
                log("file: {}, {} lines".format(filename, line_num), depth)
                total_line_num += line_num
            else:
                log("ignored: {}".format(filename), depth)
        
        for dirname in dir_list:
            log("in dir: {}".format(dirname), depth)
            total_line_num += walk(os.path.join(current_path, dirname), depth + 1)
            log("out dir: {}".format(dirname), depth)
    except:
        log("error occur!", depth)
    return total_line_num

# cc.py [--debug] [--dir-filter ...] [--ext-filter ...]
if __name__ == '__main__':
    sub_dirs : list = []
    state = 0

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            if arg == "--debug":
                debug = True
                state = 0
            elif arg == "--ext-filter":
                state = 1
            elif arg == "--dir-filter":
                state = 2
            elif arg == "--help":
                print("help: {} [--debug] [--dir-filter ...] [--ext-filter ...]".format(sys.argv[0]))
                state = 0
        else:
            if state == 1:
                list.append(filter_list, arg)
            if state == 2:
                list.append(sub_dirs, arg)
    if len(filter_list) == 0:
        filter_list = [".cpp", ".h", ".c"]
    if len(sub_dirs) == 0:
        sub_dirs = [""]

    totalLines = 0
    for sub_dir in sub_dirs:
        target_dir = os.path.join(os.getcwd(), sub_dir)
        log("dealing dir: {}".format(target_dir), 0)
        totalLines += walk(target_dir, 1)
    
    print("{} lines".format(totalLines))
    
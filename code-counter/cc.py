"""
代码统计
"""
import os
import sys

debug_mode : bool = False

def log(message, depth = 0):
    shift = depth * "    "
    if debug_mode:
        print(shift + message)

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

def count_line_num_from_file(filepath):
    count = 0
    f = open(filepath, "r", encoding='UTF-8')
    for idx, line in enumerate(f):
        if len(line) > 1:
            count += 1
    return count


def walk_impl(current_path, ext_filter, ext_filter_line_num, depth):
    try:
        dirnames, filenames = split_dir(current_path)
        for filename in filenames:
            for ext in ext_filter:
                if filename.endswith(ext):
                    line_num = count_line_num_from_file(os.path.join(current_path, filename))
                    ext_filter_line_num[ext] = ext_filter_line_num[ext] + line_num
                    log("file: {}, {} lines".format(filename, line_num), depth)
            else:
                log("ignored: {}".format(filename), depth)
        
        for dirname in dirnames:
            log("in dir: {}".format(dirname), depth)
            walk_impl(os.path.join(current_path, dirname), ext_filter, ext_filter_line_num, depth + 1)
            log("out dir: {}".format(dirname), depth)
    except:
        log("error occur!", depth)

def walk(current_path, ext_filter):
    ext_filter_line_num = {}
    for ext in ext_filter:
        if ext not in ext_filter_line_num:
            ext_filter_line_num[ext] = 0
    walk_impl(current_path, ext_filter, ext_filter_line_num, 1)
    return ext_filter_line_num

# cc.py [path] [--debug] [--help] [--dir-filter ...] [--ext-filter ...]
if __name__ == '__main__':
    dir_filter = []
    ext_filter = []
    dir_filter_line_num = {}
    state = 0
    need_help = False
    cwd = "."
    args = sys.argv[1:]

    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        cwd = sys.argv[1]
        args = sys.argv[2:]
    
    for arg in args:
        if arg.startswith("--"):
            if arg == "--debug":
                debug_mode = True
                state = 0
            elif arg == "--ext-filter":
                state = 1
            elif arg == "--dir-filter":
                state = 2
            elif arg == "--help":
                need_help = True
                state = 0
            else:
                print("unknown: {}".format(arg))
                state = 0
        else:
            if state == 1:
                list.append(ext_filter, arg)
            if state == 2:
                list.append(dir_filter, arg)
    if len(ext_filter) == 0:
        ext_filter = [".cpp", ".h", ".c"]
    if len(dir_filter) == 0:
        dir_filter = [""]
    
    log("ext-filter = {}".format(ext_filter))
    log("dir-filter = {}".format(dir_filter))
    log("cwd = {}".format(cwd))
    log("args = {}".format(args))

    if need_help:
        print("{} [path] [--debug] [--help] [--dir-filter ...] [--ext-filter ...]".format(sys.argv[0]))
        print("for example: {} ./project --debug --dir-filter src/App1 src/App2 --ext-filter .h .c .py".format(sys.argv[0]))
        print("default: ext-filter = {}, path = \".\"\n".format(ext_filter))
    
    for dir in dir_filter:
        target_dir = os.path.join(cwd, dir)
        log("dealing dir: {}".format(target_dir), 0)
        ext_filter_line_num = walk(target_dir, ext_filter)
        dir_filter_line_num[dir] = ext_filter_line_num
    
    total_line_num = 0
    for k, v in dir_filter_line_num.items():
        line_num = sum(v.values())
        if len(k) > 0:
            print("{}\t: {}\tlines".format(k, line_num))
        total_line_num = total_line_num + line_num
    
    print("Total: {} lines".format(total_line_num))
    
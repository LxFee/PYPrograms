import os

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

def walk_impl(current_path, depth):
    all_filenames = []
    dirnames, filenames = split_dir(current_path)
    for filename in filenames:
        all_filenames.append([filename])
    for dirname in dirnames:
        for filename in walk_impl(os.path.join(current_path, dirname), depth + 1):
            filename.append(dirname)
            all_filenames.append(filename)
    return all_filenames

def walk(current_path):
    return walk_impl(current_path, 1)

if __name__ == '__main__':
    dirpath = input("输入遍历目录：")
    filenames = walk(dirpath)
    for filename in filenames:
        print(filename)
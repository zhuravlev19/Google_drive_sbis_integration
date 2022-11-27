import os


def make_directory(path, name):
    os.mkdir(f"{path}\{name}")


def desktop_files_list(path):
    files_list = os.listdir(path)
    return  files_list

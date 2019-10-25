# -*- coding: utf8 -*-

import os
import shutil
from os import sys, path


def write_str_file(str, file):
    with open(file, 'w') as f:
        f.write(str)


def read_str_file(file):
    with open(file, 'r') as f:
        return f.read()


def list_dir_recur(dir):
    ret = []
    files = os.listdir(dir)
    for fi in files:
        fi_d = os.path.join(dir, fi)
        if os.path.isdir(fi_d):
            ret += list_dir_recur(fi_d)
        else:
            ret.append(fi_d)
    return ret


def copy_dir_recur(srcpath, dstpath):
    os.system("rm -rf {dstpath}".format(dstpath=dstpath))
    os.system("cp -rf {srcpath} {dstpath}".format(srcpath=srcpath, dstpath=dstpath))
    # if not os.path.exists(srcpath):
    #     print "srcpath not exist!"
    # if not os.path.exists(dstpath):
    #     print "dstpath not exist!"
    #     mkdir(dir)
    # for root, dirs, files in os.walk(srcpath, True):
    #     for eachfile in files:
    #         shutil.copy(os.path.join(root, eachfile), dstpath)


def mkdir(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            os.rmdir(dir)
        else:
            os.remove(dir)
    os.mkdir(dir)


if __name__ == '__main__':
    mkdir("aa")

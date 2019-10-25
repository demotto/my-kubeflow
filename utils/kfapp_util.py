# -*- coding: utf8 -*-

import commands
import re
import os
from os import sys, path
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from conf import env_conf
import k8s_util
import file_util
import docker_util

replace_prefix = [
    'gcr.io/'
]

username = env_conf.global_params['docker']['username']
image_prefix = "{username}/mykubeflow.".format(username=username)


def replace_image(file):
    content = file_util.read_str_file(file)
    for prefix in replace_prefix:
        pattern = r"{prefix}.*".format(prefix=prefix)
        addrs = re.findall(pattern, content)
        addrs = set(addrs)
        for addr in addrs:
            new_addr = image_prefix + addr.replace("/", ".")
            content = content.replace(addr, new_addr)
            docker_util.image_pull_v2(addr)
            docker_util.image_tag_v2(addr, new_addr)
            docker_util.image_push_v2(new_addr)
    file_util.write_str_file(content, file)


def create_my_kfapp():
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/kfapp"
    my_kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/my-kfapp"
    file_util.copy_dir_recur(kfapp_dir, my_kfapp_dir)
    files = file_util.list_dir_recur(my_kfapp_dir)
    for file in files:
        print(file)
        replace_image(file)


def install():
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/my-kfapp"
    app_file = kfapp_dir + "/app.yaml"
    template = file_util.read_str_file(app_file)
    content = template.replace("your_app_dir", kfapp_dir)

    file_util.write_str_file(content, app_file)
    cmd = "cd {kfapp_dir}; kfctl apply all -V".format(kfapp_dir=kfapp_dir)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception("run command error")
    print(output)


if __name__ == '__main__':
    create_my_kfapp()
    #install()

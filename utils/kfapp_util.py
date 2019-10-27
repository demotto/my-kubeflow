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
nfs_server = env_conf.global_params['nfs']['server']
nfs_path = env_conf.global_params['nfs']['path']

def is_image_need_replaced(image):
    for p in replace_prefix:
        if image.startswith(p):
            return True
    return False


def replace_image(file):
    content = file_util.read_str_file(file)
    for prefix in replace_prefix:
        pattern = r"image: {prefix}.*".format(prefix=prefix)
        addrs = re.findall(pattern, content)
        addrs = set(addrs)
        for addr in addrs:
            addr = addr.lstrip('image:').strip()
            new_addr = image_prefix + addr.replace("/", ".")
            content = content.replace(addr, new_addr)
            # if "$(project)" not in addr:
            #     docker_util.image_pull_v2(addr)
            #     docker_util.image_tag_v2(addr, new_addr)
            #     docker_util.image_push_v2(new_addr)
        pattern = r"{prefix}.*".format(prefix=prefix)
        addrs = re.findall(pattern, content)
        addrs = set(addrs)
        for addr in addrs:
            addr = addr.strip()
            new_addr = image_prefix + addr.replace("/", ".")
            content = content.replace(addr, new_addr)
    file_util.write_str_file(content, file)


def create_my_kfapp():
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/kfapp"
    my_kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/my-kfapp"
    file_util.copy_dir_recur(kfapp_dir, my_kfapp_dir)
    files = file_util.list_dir_recur(my_kfapp_dir)
    for file in files:
        print(file)
        replace_image(file)

    app_file = my_kfapp_dir + "/app.yaml"
    template = file_util.read_str_file(app_file)
    content = template.replace("your_app_dir", my_kfapp_dir)
    file_util.write_str_file(content, app_file)


def scan_kfapp():
    images = []
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/kfapp"
    files = file_util.list_dir_recur(kfapp_dir)
    for f in files:
        if not f.endswith(".yaml"):
            continue
        docs = file_util.read_yaml_file(f)
        for doc in docs:
            if "images" in doc:
                for image in doc['images']:
                    name = image['name']
                    tag = image['newTag']
                    addr = name + ":" + tag
                    if is_image_need_replaced(addr):
                        images.append(addr)
        content = file_util.read_str_file(f)
        for prefix in replace_prefix:
            pattern = r"image: {prefix}.*".format(prefix=prefix)
            addrs = re.findall(pattern, content)
            addrs = set(addrs)
            for addr in addrs:
                addr = addr.lstrip('image:').strip()
                if "$(project)" not in addr and is_image_need_replaced(addr) and image_has_tag(addr):
                    images.append(addr)
    images = set(images)
    return images


def conver_image_addr(addr):
    return image_prefix + addr.replace("/", ".").strip()


def image_has_tag(addr):
    return ":" in addr


def install():
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/my-kfapp"
    cmd = "cd {kfapp_dir}; kfctl apply all -V".format(kfapp_dir=kfapp_dir)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception("run command error", output)
    print(output)


def replace_pv():
    kfapp_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/kfapp"
    files = file_util.list_dir_recur(kfapp_dir)
    for f in files:
        if f.endswith("persistent-volume.yaml"):
            docs = file_util.read_yaml_file(f)
            for doc in docs:
                spec = doc['spec']
                spec.pop('gcePersistentDisk')
                nfs_config = {
                    "path": nfs_path + "/" + doc['metadata']['name'],
                    "server": nfs_server
                }
                spec['nfs'] = nfs_config
                doc['spec'] = spec
                my_f = f.replace("/kfapp/", "/my-kfapp/")
                file_util.write_yaml_file(doc, my_f)
                break


if __name__ == '__main__':
    replace_pv()

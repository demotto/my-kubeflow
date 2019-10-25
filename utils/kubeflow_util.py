import commands
import re
import os
from os import sys, path
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import docker_util
import k8s_util
import file_util



def _check(ns):
    """Check if kubeflow is installed; if not, raise an exception."""
    cmd = "kubectl get ns {ns}".format(ns=ns)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)


def _analyze_image(image):
    pass


def _export_deploy(deploy_name, ns="kubeflow"):
    cmd_template = "kubectl get deployment {deploy_name} -n {ns} -o yaml"
    pass


def _replace_images():
    pass


def __retrieve_image_infos(content):
    image_infos = []
    pattern = r"image: (.*)"
    results = re.findall(pattern, content)
    image_set = set(results)
    for image in image_set:
        arr = image.split(":")
        image_infos.append((arr[0], arr[1]))
    return image_infos


def __generate_new_image_info(image_info):
    from conf import env_conf
    username = env_conf.global_params['docker']['username']
    prefix = "{username}/mykubeflow.".format(username=username)
    image_id = image_info[0]
    image_tag = image_info[1]
    new_image_id = prefix + image_id.replace("/", ".")
    new_image_tag = image_tag
    return new_image_id, new_image_tag


def diy_deploys(ns):
    docker_util.login()
    deploy_names = k8s_util.list_deploys(ns)
    for deploy_name in deploy_names:
        content = k8s_util.get_deploy_yaml(deploy_name, ns)
        image_infos = __retrieve_image_infos(content)
        print(image_infos)
        for image_info in image_infos:
            image_id = image_info[0]
            image_tag = image_info[1]
            new_image_id, new_image_tag = __generate_new_image_info(image_info)
            new_image = new_image_id + ":" + new_image_tag
            docker_util.image_pull(image_id, image_tag)
            docker_util.image_tag(image_id, image_tag, new_image_id, new_image_tag)
            docker_util.image_push(new_image_id, new_image_tag)
            content = content.replace(image_id + ":" + image_tag, new_image)
        output_path = path.dirname(path.dirname(path.abspath(__file__))) + "/deploy/" + deploy_name + ".yaml"
        file_util.write_str_file(content, output_path)

def diy_kfapp():
    pass

def remove_kubeflow(ns):
    cmd = "kubectl delete ns {ns} --grace-period=0 --force".format(ns=ns)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    return output


def install_kubeflow(ns):
    k8s_util.create_namespace(ns)
    deploy_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/deploy"
    deploy_files = os.listdir(deploy_dir)
    deploy_cmd = "kubectl create "
    for deploy_file in deploy_files:
        if deploy_file.endswith(".yaml"):
            full_path = deploy_dir + "/" + deploy_file
            deploy_cmd += " -f " + full_path
    print(deploy_cmd)
    (status, output) = commands.getstatusoutput(deploy_cmd)
    if status != 0:
        raise Exception(output)
    return output


if __name__ == "__main__":
    #diy_deploys("kubeflow")
    install_kubeflow("kubeflow")


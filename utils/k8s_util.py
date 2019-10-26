import commands
import os
from os import sys, path

import ssh_util

def _check():
    """Check if kubectl works well; if not, raise Exception."""
    cmd = "kubectl get nodes"
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)


def list_deploys(ns):
    cmd = "kubectl get deployments -n {ns}".format(ns=ns)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception("run command error")
    lines = output.split("\n")
    ret = []
    for i in range(1, len(lines)):
        line = lines[i]
        cols = line.split(" ")
        ret.append(cols[0])
    return ret


def get_deploy_yaml(deploy_name, ns):
    cmd = "kubectl get deployment {deploy_name} -n {ns} -o yaml".format(
        deploy_name=deploy_name,
        ns=ns
    )
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    return output


def create_namespace(ns):
    cmd = "kubectl create namespace {ns}".format(ns=ns)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    return output


def add_worker(worker_name):
    cmd_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/k8s"
    ssh_util.ssh_copy(cmd_dir, "/tmp", worker_name)
    join_cmd = create_join_command()
    print(join_cmd)


def create_join_command():
    cmd_dir = path.dirname(path.dirname(path.abspath(__file__))) + "/k8s"
    cmd = cmd_dir + "/create_kubectl_join.sh"
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    return output.strip()


def remove_worker(worker_name):
    pass


if __name__ == '__main__':
    add_worker("store05")

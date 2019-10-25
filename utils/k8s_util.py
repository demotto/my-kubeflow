import commands


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


if __name__ == '__main__':
    _check()
    content = get_deploy_yaml("workflow-controller", "kubeflow")
    print(content)

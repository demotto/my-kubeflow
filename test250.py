from utils import file_util
import yaml

y = file_util.read_str_file("D:/caocao/my-kubeflow/kfapp/kustomize/api-service/base/kustomization.yaml")
#y = file_util.read_str_file("D:/caocao/my-kubeflow/kfapp/kustomize/argo/base/cluster-role-binding.yaml")
y = yaml.safe_load_all(y)
for doc in y:
    print(type(doc))

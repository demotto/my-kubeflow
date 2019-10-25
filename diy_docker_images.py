from utils import kfapp_util
from utils import file_util
from utils import docker_util


def diy_docker_images():
    images = kfapp_util.scan_kfapp()
    print(images)
    records = []
    for image in images:
        new_image = kfapp_util.conver_image_addr(image)
        records.append({"image": image, "new_image": new_image})
    record_path = "images/records.yaml"
    file_util.write_yaml_file(records, record_path)

    for record in records:
        image = record['image']
        new_image = record['new_image']
        docker_util.image_pull_v2(image)
        docker_util.image_tag_v2(image, new_image)
        docker_util.image_push_v2(new_image)


if __name__ == '__main__':
    diy_docker_images()

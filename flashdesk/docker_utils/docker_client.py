import docker
import json
from datetime import datetime

client = docker.from_env()

DOCKER_EXISTS = False


def check_if_docker_exists():
    global DOCKER_EXISTS
    if bool(client.version()):
        DOCKER_EXISTS = True
        return DOCKER_EXISTS
    else:
        return DOCKER_EXISTS


def start_container_using_image_id(image_id):
    container = client.containers.run(
        image=image_id, detach=True, ports={"5901": "5901", "6901": "6901"}
    )
    print(container.short_id)
    return container.short_id


def kill_container_using_container_id(container_id):
    client.containers.get(container_id).kill()


def get_all_filesystem_docker_images():
    try:
        images = client.images.list()
        image_list = []
        for image in images:
            image_info = {
                "image_id": image.id,
                "short_id": image.short_id,
                "labels": image.labels,
                "tags": image.tags,
                "created": image.attrs["Created"],
                "size": image.attrs["Size"],
                "architecture": image.attrs["Architecture"],
                "os":image.attrs["Os"]
            }
            image_list.append(image_info)
        return image_list
    except docker.errors.APIError as e:
        print("Error:", e)
        return []


def docker_search(query):
    try:
        search_results = client.images.search(query)
        return search_results
    except docker.errors.DockerException as e:
        print("Error:", e)
        return []

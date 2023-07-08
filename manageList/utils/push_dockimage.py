import subprocess
import docker

def push_docker_image(image):
    # Set the Azure Container Registry (ACR) details
    registry = 'srs2023.azurecr.io'
    repository = 'samples'
    image_tag = image

    # Create a Docker client
    client = docker.from_env()

    # Tag the local image with the ACR repository and tag
    acr_image = f'{registry}/{repository}/{image_tag}'
    client.images.get(image).tag(acr_image)

    # Push the image to the ACR
    client.images.push(acr_image)

    # Optionally, remove the local image
    client.images.remove(acr_image)






# Building standard docker in CONCERT
# (Using Xbot2_docker)

This guide is meant to have a standardize building of the dockers for concerta cross all its machine (embedded, control and vision).
We will provide default instruction, whereas more costum installation can be done after the creation of the docker.
Please don't mess with dockers of others :)

## Getting started
We use Xbot2_docker as base generation, with some sanity checks. Please refer to that pacage for extensive explaining.

## Creating the docker
clone the repo and enter the correct direcotry. We assume Ubuntu 24.04 and ROS2 Jazzy.
```bash
git clone <repo>
cd xbot2_docker/noble
```
> [!WARNING]
> If you need to attach some external devices to the host machine and let them be read by the host (i.e. **realsense**), probably you'll need to add the volume `/dev:/dev:r` in the correct service inside compose.yaml

Now create the docker.
>[!CAUTION]
> If you will use the GPU of the host machine (NVIDIA), you'll need to build the **`robot-nvidia`** service, with `robot` otherwise.

```bash
# Update the image
docker compose pull <service_name>
#Bring up the container
docker compose -p <name> up -d robot-nvidia
```

> [!NOTE]
> Notice that previously we associated the docker container a name. We can use that name to identify it by "tabbing" after a -p flag in docker.
> Also that nome will be "composed with the service name to form the docker container's name.
> *For instance the name "test" used with the service "robot-nvidia" will generate the container named "test-robot-nvidia-1".*

Now you docker is ready and to enter the container from a terminal you can use from inside the current folder:
```bash
docker compose exec -p <name> exec <service_name> bash
```
or from wherever in the machine with:
```bash
docker exec -it <container_name> exec bash
```
> [!NOTE]
> After -p and -it flag you can just tab to see the available options

## Inside the container
Inside the container basically you can do whatever you want. For the sake of clarity, we should keep track of the important container created in each machine in this file [link to file]. Adding also a small description of what the container uses or the intent might be good.<br>

### Some example
In the folder examples you'll find two readme with the commands to create a basic docker for each CONCERT on board host (assuming all the recipes of forest are up-to date).

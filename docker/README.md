# Standard Docker Setup for CONCERT

This guide describes the recommended procedure for creating and managing Docker containers across the CONCERT machines:

* Embedded
* Control
* Vision

The containers are based on the `xbot2_docker` repository.

The goal is to keep the setup consistent across all machines while still allowing host-specific customization after container creation.

> [!IMPORTANT]
> Do not modify, stop, or remove containers belonging to other users unless previously agreed.

## Requirements

This guide assumes:

* Ubuntu 24.04 Noble
* ROS 2 Jazzy
* Docker Engine
* Docker Compose
* NVIDIA Container Toolkit when GPU access is required

## Getting started

Clone the `xbot2_docker` repository and enter the Noble configuration directory:

```bash
git clone <repository-url>
cd xbot2_docker/noble
```

Refer to the upstream `xbot2_docker` documentation for a complete explanation of the available services, images, and configuration options.

## Choosing the service

Use the appropriate Docker Compose service depending on the required hardware support.

| Requirement            | Service        |
| ---------------------- | -------------- |
| Standard CPU container | `robot`        |
| NVIDIA GPU access      | `robot-nvidia` |

> [!CAUTION]
> When GPU access is required, use the `robot-nvidia` service and ensure that the NVIDIA Container Toolkit is correctly installed on the host.

## Accessing host devices

When the container must access devices connected to the host, such as a RealSense camera, expose the required device paths in `compose.yaml`.

For example:

```yaml
services:
  robot-nvidia:
    volumes:
      - /dev:/dev
```

A more restrictive mapping should be preferred when the exact device is known:

```yaml
services:
  robot-nvidia:
    devices:
      - /dev/video0:/dev/video0
```

The exact device path depends on the hardware and driver configuration.

## Creating a container

First, update the base image:

```bash
docker compose pull <service-name>
```

Then create the container using a unique Compose project name:

```bash
docker compose -p <project-name> up -d <service-name>
```

Example:

```bash
docker compose -p test up -d robot-nvidia
```

Docker Compose combines the project name, service name, and replica index to generate the container name.

For example:

```text
Project name: test
Service name: robot-nvidia
Container name: test-robot-nvidia-1
```

Using a project name is important because it allows multiple containers to be created from the same Compose service without conflicts.

## Entering the container

From the directory containing `compose.yaml`:

```bash
docker compose -p <project-name> exec <service-name> bash
```

Example:

```bash
docker compose -p test exec robot-nvidia bash
```

From any directory, using the generated container name:

```bash
docker exec -it <container-name> bash
```

Example:

```bash
docker exec -it test-robot-nvidia-1 bash
```

> [!NOTE]
> Shell completion may suggest available project names, services, and container names when pressing `Tab`.

## Stopping a container

To stop a Compose project without removing its container:

```bash
docker compose -p <project-name> stop
```

To stop and remove only that Compose project:

```bash
docker compose -p <project-name> down
```

Example:

```bash
docker compose -p test down
```

This does not affect containers created using other project names, even when they use the same service.

## Container documentation

All relevant containers should be recorded in:

```text
DOCKER_LOG.md
```

For each container, document at least:

* Host machine
* Container name
* Compose project name
* Compose directory
* Creation date
* Current status
* Purpose
* Creator
* Known limitations

Host-specific installation and configuration instructions should be stored in:

```text
examples/
```

## Examples

The `examples` directory contains setup notes for specific CONCERT containers.

Current example:

```text
examples/vision_defection_robot_nvidia_1.md
```

These instructions assume that the required Forest recipes and repositories are available and up to date.

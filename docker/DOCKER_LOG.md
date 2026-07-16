# CONCERT Docker Inventory

This document tracks the main Docker containers created on each CONCERT machine.

Update this file whenever a relevant container is created, replaced, deprecated, or removed.

## Status values

Use one of the following values:

* `Active`: currently used
* `Testing`: used for development or validation
* `Deprecated`: no longer recommended
* `Stopped`: retained but not currently running
* `Removed`: container no longer exists

## Control host

| Container name | Status | Compose project | Compose directory | Creation date | Deprecation date | Description                        | Creator |
| -------------- | ------ | --------------- | ----------------- | ------------- | ---------------- | ---------------------------------- | ------- |
| —              | —      | —               | —                 | —             | —                | No container currently documented. | —       |

## Embedded host

| Container name | Status | Compose project | Compose directory | Creation date | Deprecation date | Description                        | Creator |
| -------------- | ------ | --------------- | ----------------- | ------------- | ---------------- | ---------------------------------- | ------- |
| —              | —      | —               | —                 | —             | —                | No container currently documented. | —       |

## Vision host

| Container name             | Status | Compose project | Compose directory                  | Creation date | Deprecation date | Description                                                                                                     | Creator     |
| -------------------------- | ------ | --------------- | ---------------------------------- | ------------- | ---------------- | --------------------------------------------------------------------------------------------------------------- | ----------- |
| `noble-robot-nvidia-1` | Active | `noble`     | `/home/concert/xbot2_docker/noble` | 2026-07-17    | —                | Standard GPU-enabled container with RealSense support. Used for localization and navigation. | `alelovato` |

## Notes

When replacing an existing container, do not delete its row. Mark it as `Deprecated` or `Removed`, record the relevant date, and add the replacement container as a new entry.

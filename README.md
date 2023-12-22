# Trace Sensor Installation Client

## Description
 This module is used for generating a binary package for linux systems which can hosted at a Package Repository such as Advanced Package Tool (APT) Repository or can directly install using package manager such as Debian Package Manager (dpkg).
 
## Directory Structure

| S.No   | Component Name                        | Directory                         |
|--------|---------------------------------------|-----------------------------------|
| 1      | Trace Sensor Installation Client      | trace-client_1.8.0-bullseye_amd64 |

## Deployment Steps

To build a binary package use the following command. 

| Command                                        |
|------------------------------------------------|
| dpkg–deb --build < Name of the Package Directory >|

## Developer Notes
* Client Location Information via - not yet integrated 
* Binary needs to be pythonised


# TRACE Containers
This repository contains the files required to build the containers required for the TRACE product.

# Directory Structure


| S.No   | Component Name   | Directory   |
|--------|------------------|-------------|
| 1      | Build Files      | build_files |
| 2      | Analytics Files  | analytics   |
| 3      | Honeypots Files  | honeypots   |
| 4      | Monitor Files    | monitor     |

Desrciption of Components

1. Build Files : This folder contains the build files required for building containers.
2. Analytics Files : This folder contains the containers required for building the analytics components of the trace-net service of TRACE.
3. Honeypots Files : This folder contains the containers required for building the deception components of the trace-net service of TRACE.
4. Monitor Files : This folder contains the containers required for building the trace-monitor service of TRACE.


# Developer Note

* Currently the Index name on which the data sent is hardcoded. This will be updated to dynamic in the future release.

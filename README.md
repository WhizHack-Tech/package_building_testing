# HIDS Host Installation Client

## Description
 This module is used for generating a binary package for linux systems which can hosted at a Package Repository such as Advanced Package Tool (APT) Repository or can directly install using package manager such as Debian Package Manager (dpkg).
 
## Directory Structure

| S.No   | Component Name                        | Directory                          |
|--------|---------------------------------------|------------------------------------|
| 1      | HIDS Manager Installation Client         | xdr-hids-manager_1.0.0-bullsye_amd64 |

## Deployment Steps

To build a binary package use the following command. 

| Command                                                |
|--------------------------------------------------------|
| sudo dpkg–deb --build < Name of the Package Directory >|

To install a binary package use the following command. 

| Command                                                |
|--------------------------------------------------------|
| sudo apt install ./< Name of the Binary Package >      |

## Developer Notes
* Client Location Information via - not yet integrated 
* Binary needs to be pythonise
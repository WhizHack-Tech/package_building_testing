# Photon

The photon project is a lightweight and superfast DPI engine written in golang.<br>

This is a passive utility which listens and analyses the network traffic while extracting any threat indicators from the live traffic.
The main goal is to provide security researchers with more insights on the alerts they are receiving.
The photon engine is capable of performing packet analysis, stream analysis and network asset profilling from live network traffic.
It also provides capability to extract reconstructed files and artifacts from network traffic.

What is the photon capable of?

## Features

The photon engine boasts of the following features which can be used for training AI and ML engines.

1. Extraction of streams from network traffic.
2. Extraction of packet data from network traffic.
3. Labelling of network thretas based on provided threat feeds.
4. Extraction of files and artifacts from network data.

## Installation

### Dependencies?
The project depends on the famous libpcap library and has support only for Linux systems, currently we have no plans to provide support for Windows platform.<br>

### I cannot locate the executable binary.

To build your own binary follow these steps.
1. Install go in your system enter the project directory using a command line.
2. go mod init
3. go mod tidy
4. go build

## Authors
Lakshy Sharma<br>
Mahesh Banerjee
/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The aim of the photon project is to create a high speed packet analyser capable of capturing packets in high throughput networks and provide real time analysis for each packet.
	The project aims to provide a rich quality dataset for processing network packet data using AI and machine learning.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package main

import (
	"flag"
	"photon/wavelets"
)

func main() {
	// These are flag variables which are used for configuring the capture metrics.
	wavelets.InitVariables.CaptureInterface = flag.String("i", "eth0", "Interface to capture packets.")
	wavelets.InitVariables.SnapshotLength = flag.Int("s", 65535, "SnapLen for pcap packet capture")
	wavelets.InitVariables.CollectArtifacts = flag.Bool("collect_artifacts", false, "Enable collection of artifacts from reassembled packets. (WARNING! High memory consumption)")
	wavelets.InitVariables.CaptureEnvironment = flag.String("operation_environment", "generic", "Set the capture environment to label the data for future analysis.")
	wavelets.InitVariables.CaptureMode = flag.String("operation_mode", "complete", "There are three modes. 1. complete: Use all analysis methods. 2. profiling: Perform only profile analysis. 3. dpi: Perform only dpi based research analysis.")
	flag.Parse()
	wavelets.PhotonRouter()
}

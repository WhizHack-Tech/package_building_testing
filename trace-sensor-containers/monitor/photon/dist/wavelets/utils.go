/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The utils file is usefull for storing miscellaneous code that comes in handy to expedite development elsewhere.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package wavelets

import (
	"strings"

	"github.com/syrinsecurity/gologger"
)

// Given a set of ports and a protocol type.
// This function detects the type of service that might be running.
func detectServiceName(srcPort int, dstPort int, serviceType string) string {
	var srcMatchExists bool
	var srcMatch string
	var dstMatchExists bool
	var dstMatch string
	var serviceName string

	if serviceType == "UDP" {
		srcMatch, srcMatchExists = udpMap[srcPort]
		dstMatch, dstMatchExists = udpMap[dstPort]
	} else if serviceType == "SCTP" {
		srcMatch, srcMatchExists = sctpMap[srcPort]
		dstMatch, dstMatchExists = sctpMap[dstPort]
	} else if serviceType == "TCP" {
		srcMatch, srcMatchExists = tcpMap[srcPort]
		dstMatch, dstMatchExists = tcpMap[dstPort]
	}

	if srcMatch == dstMatch {
		serviceName = srcMatch
	} else if srcMatchExists && !dstMatchExists {
		serviceName = srcMatch
	} else if !srcMatchExists && dstMatchExists {
		serviceName = dstMatch
	} else {
		serviceName = "N/A"
	}

	return serviceName
}

// This function analyses a provided payload string.
func payloadStringAnalyser(payloadString string) string {
	var analysis string

	if strings.Contains(payloadString, "googlecast") {
		analysis = "Detected a Chromecast Device."
	} else if strings.Contains(payloadString, "airplay") {
		analysis = "Detected Apple Airplay Device"
	} else if strings.Contains(payloadString, "MAILSLOT") && strings.Contains(payloadString, "SMB") {
		analysis = "Detected a NetBIOS Broadcast message"
	} else if strings.Contains(payloadString, "spotify") {
		analysis = "Detected a Spotify Broadcast Message"
	} else if strings.Contains(payloadString, "dlink") {
		analysis = "Detected a D link device"
	}
	return analysis
}

// Extract unique string values from a slice.
func getUniqueSliceValues(stringSlice []string) []string {
	keys := make(map[string]bool)
	list := []string{}
	for _, entry := range stringSlice {
		if _, value := keys[entry]; !value {
			keys[entry] = true
			list = append(list, entry)
		}
	}
	return list
}

// Extract unique int values from a slice.
func getUniqueSliceValuesInt(intSlice []uint32) []uint32 {
	keys := make(map[uint32]bool)
	list := []uint32{}
	for _, entry := range intSlice {
		if _, value := keys[entry]; !value {
			keys[entry] = true
			list = append(list, entry)
		}
	}
	return list
}

// Get maximum value from a provided integer slice.
func getMaxIntSlice(intSlice []uint32) uint32 {
	max := intSlice[0]
	for _, int := range intSlice {
		if int > max {
			max = int
		}
	}
	return max
}

// Create a logger whenever required.
func createLogger(outputfile string) gologger.Logger {
	logger, err := gologger.New(outputfile, 3000)
	if err != nil {
		panic(err)
	}
	return logger
}

/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The profiler file is useful for analysing each individual packet and creating network profile for each and every IP it discovers.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package wavelets

import (
	"encoding/json"
	"strings"
	"time"
	"unicode"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
)

// This function analyses a packet and sends the collected device data for further analysis.
func analysePacket(packetData profilerInputChannel) deviceProfile {
	var deviceData deviceProfile

	switch packetData.packetType {
	case "normal-packet":
		for _, typ := range packetData.decodedLayers {
			switch typ {
			case layers.LayerTypeEthernet:
				deviceData.DeviceMac = ethLayer.SrcMAC.String()
				deviceData.RelationMacs = append(deviceData.RelationMacs, ethLayer.DstMAC.String())
			case layers.LayerTypeIPv4:
				deviceData.DeviceIP = ipLayer.SrcIP.String()
				deviceData.RelationIPs = append(deviceData.RelationIPs, ipLayer.DstIP.String())
			case layers.LayerTypeUDP:
				serviceName := detectServiceName(int(udpLayer.SrcPort), int(udpLayer.DstPort), "UDP")
				if _, exists := deviceData.ServiceVolumes[serviceName]; !exists {
					// If the service name doesnt exist in the map then create a new entry.
					deviceData.ServiceVolumes = make(map[string]int)
					deviceData.ServiceVolumes[serviceName] = 1
				} else {
					// If the service name exists in the map then increment current value.
					deviceData.ServiceVolumes[serviceName] += 1
				}
			case layers.LayerTypeDNS:
				// Capturing DNS data.
				if dnsLayer.Questions != nil {
					for _, questionDetails := range dnsLayer.Questions {
						deviceData.DnsQuestions = append(deviceData.DnsQuestions, string(questionDetails.Name))
					}
				}
				if dnsLayer.Answers != nil {
					for _, answerDetails := range dnsLayer.Answers {
						deviceData.DnsAnswers = append(deviceData.DnsAnswers, string(answerDetails.Name))
					}
				}
				// Cleaning DNS data.
				deviceData.DnsQuestions = getUniqueSliceValues(deviceData.DnsQuestions)
				deviceData.DnsAnswers = getUniqueSliceValues(deviceData.DnsAnswers)
			case gopacket.LayerTypePayload:
				payloadData := packetPayload.LayerContents()

				payloadString := strings.Map(func(r rune) rune {
					if unicode.IsPrint(r) {
						return r
					}
					return -1
				}, string(payloadData))
				deviceData.Payloads = append(deviceData.Payloads, payloadString)
			}
		}
	case "vxlan-packet":
		for index, typ := range packetData.decodedLayers {
			if index >= 4 {
				switch typ {
				case layers.LayerTypeEthernet:
					deviceData.DeviceMac = ethLayer.SrcMAC.String()
					deviceData.RelationMacs = append(deviceData.RelationMacs, ethLayer.DstMAC.String())
				case layers.LayerTypeIPv4:
					deviceData.DeviceIP = ipLayer.SrcIP.String()
					deviceData.RelationIPs = append(deviceData.RelationIPs, ipLayer.DstIP.String())
				case layers.LayerTypeUDP:
					serviceName := detectServiceName(int(udpLayer.SrcPort), int(udpLayer.DstPort), "UDP")
					if _, exists := deviceData.ServiceVolumes[serviceName]; !exists {
						// If the service name doesnt exist in the map then create a new entry.
						deviceData.ServiceVolumes = make(map[string]int)
						deviceData.ServiceVolumes[serviceName] = 1
					} else {
						// If the service name exists in the map then increment current value.
						deviceData.ServiceVolumes[serviceName] += 1
					}
				case layers.LayerTypeDNS:
					// Capturing DNS data.
					if dnsLayer.Questions != nil {
						for _, questionDetails := range dnsLayer.Questions {
							deviceData.DnsQuestions = append(deviceData.DnsQuestions, string(questionDetails.Name))
						}
					}
					if dnsLayer.Answers != nil {
						for _, answerDetails := range dnsLayer.Answers {
							deviceData.DnsAnswers = append(deviceData.DnsAnswers, string(answerDetails.Name))
						}
					}
					// Cleaning DNS data.
					deviceData.DnsQuestions = getUniqueSliceValues(deviceData.DnsQuestions)
					deviceData.DnsAnswers = getUniqueSliceValues(deviceData.DnsAnswers)
				case gopacket.LayerTypePayload:
					payloadData := packetPayload.LayerContents()

					payloadString := strings.Map(func(r rune) rune {
						if unicode.IsPrint(r) {
							return r
						}
						return -1
					}, string(payloadData))
					deviceData.Payloads = append(deviceData.Payloads, payloadString)
				}
			}
		}
	case "normal-stream":
		globalFsmErrorAcceptFlag = false
		for _, typ := range packetData.decodedLayers {
			switch typ {
			case layers.LayerTypeEthernet:
				deviceData.DeviceMac = ethLayer.SrcMAC.String()
				deviceData.RelationMacs = append(deviceData.RelationMacs, ethLayer.DstMAC.String())
			case layers.LayerTypeIPv4:
				deviceData.DeviceIP = ipLayer.SrcIP.String()
				deviceData.RelationIPs = append(deviceData.RelationIPs, ipLayer.DstIP.String())
			case layers.LayerTypeTCP:
				serviceName := detectServiceName(int(tcpLayer.SrcPort), int(tcpLayer.DstPort), "TCP")
				if _, exists := deviceData.ServiceVolumes[serviceName]; !exists {
					// If the service name doesnt exist in the map then create a new entry.
					deviceData.ServiceVolumes = make(map[string]int)
					deviceData.ServiceVolumes[serviceName] = 1
				} else {
					// If the service name exists in the map then increment current value.
					deviceData.ServiceVolumes[serviceName] += 1
				}
			case layers.LayerTypeDNS:
				// Capturing DNS data.
				if dnsLayer.Questions != nil {
					for _, questionDetails := range dnsLayer.Questions {
						deviceData.DnsQuestions = append(deviceData.DnsQuestions, string(questionDetails.Name))
					}
				}
				if dnsLayer.Answers != nil {
					for _, answerDetails := range dnsLayer.Answers {
						deviceData.DnsAnswers = append(deviceData.DnsAnswers, string(answerDetails.Name))
					}
				}
				// Cleaning DNS data.
				deviceData.DnsQuestions = getUniqueSliceValues(deviceData.DnsQuestions)
				deviceData.DnsAnswers = getUniqueSliceValues(deviceData.DnsAnswers)
			case gopacket.LayerTypePayload:
				payloadData := packetPayload.LayerContents()

				payloadString := strings.Map(func(r rune) rune {
					if unicode.IsPrint(r) {
						return r
					}
					return -1
				}, string(payloadData))
				deviceData.Payloads = append(deviceData.Payloads, payloadString)
			}
		}
	case "vxlan-stream":
		globalFsmErrorAcceptFlag = true
		for index, typ := range packetData.decodedLayers {
			if index >= 4 {
				switch typ {
				case layers.LayerTypeEthernet:
					deviceData.DeviceMac = ethLayer.SrcMAC.String()
					deviceData.RelationMacs = append(deviceData.RelationMacs, ethLayer.DstMAC.String())
				case layers.LayerTypeIPv4:
					deviceData.DeviceIP = ipLayer.SrcIP.String()
					deviceData.RelationIPs = append(deviceData.RelationIPs, ipLayer.DstIP.String())
				case layers.LayerTypeTCP:
					serviceName := detectServiceName(int(tcpLayer.SrcPort), int(tcpLayer.DstPort), "TCP")
					if _, exists := deviceData.ServiceVolumes[serviceName]; !exists {
						// If the service name doesnt exist in the map then create a new entry.
						deviceData.ServiceVolumes = make(map[string]int)
						deviceData.ServiceVolumes[serviceName] = 1
					} else {
						// If the service name exists in the map then increment current value.
						deviceData.ServiceVolumes[serviceName] += 1
					}
				case layers.LayerTypeDNS:
					// Capturing DNS data.
					if dnsLayer.Questions != nil {
						for _, questionDetails := range dnsLayer.Questions {
							deviceData.DnsQuestions = append(deviceData.DnsQuestions, string(questionDetails.Name))
						}
					}
					if dnsLayer.Answers != nil {
						for _, answerDetails := range dnsLayer.Answers {
							deviceData.DnsAnswers = append(deviceData.DnsAnswers, string(answerDetails.Name))
						}
					}
					// Cleaning DNS data.
					deviceData.DnsQuestions = getUniqueSliceValues(deviceData.DnsQuestions)
					deviceData.DnsAnswers = getUniqueSliceValues(deviceData.DnsAnswers)
				case gopacket.LayerTypePayload:
					payloadData := packetPayload.LayerContents()

					payloadString := strings.Map(func(r rune) rune {
						if unicode.IsPrint(r) {
							return r
						}
						return -1
					}, string(payloadData))
					deviceData.Payloads = append(deviceData.Payloads, payloadString)
				}
			}
		}
	}
	return deviceData
}

// This function searches for a record in a list.
func searchRecord(records []deviceProfile, Identifier string) (int, bool) {
	// Iterate over current records and search if provided device mac is found in the data.
	for index, element := range records {
		if element.DeviceMac == Identifier {
			return index, true
		}
	}
	
	return -1, false
}

// This function takes the analysed data from the packet analyser and searches the current database for relevant records.
// Once a matching record is found we append the data to that record or create a new one.
func appendRecord(currentRecords []deviceProfile, deviceData deviceProfile) []deviceProfile {
	Identifier := deviceData.DeviceMac
	if index, exists := searchRecord(currentRecords, Identifier); exists {
		// If search record returns a true value then append the data to the record we had added earlier.
		currentRecords[index].RelationIPs = append(currentRecords[index].RelationIPs, deviceData.RelationIPs...)
		currentRecords[index].RelationMacs = append(currentRecords[index].RelationMacs, deviceData.RelationMacs...)
		currentRecords[index].DnsQuestions = append(currentRecords[index].DnsQuestions, deviceData.DnsQuestions...)
		currentRecords[index].DnsAnswers = append(currentRecords[index].DnsAnswers, deviceData.DnsAnswers...)
		currentRecords[index].Payloads = append(currentRecords[index].Payloads, deviceData.Payloads...)
		for serviceName, count := range deviceData.ServiceVolumes {
			if _, exists := currentRecords[index].ServiceVolumes[serviceName]; !exists {
				// If the service name doesnt exist in the map then create a new entry.
				currentRecords[index].ServiceVolumes = make(map[string]int)
				currentRecords[index].ServiceVolumes[serviceName] = count
			} else {
				// If the service name exists in the map then increment current value.
				currentRecords[index].ServiceVolumes[serviceName] += count
			}
		}
	} else {
		// If no record exists then create a new record.
		currentRecords = append(currentRecords, deviceData)
	}
	return currentRecords
}

// A simple function that cleans all created profiles.
func cleanRecords(currentRecords []deviceProfile) []deviceProfile {
	var modifiedRecords []deviceProfile
	for _, record := range currentRecords {
		record.RelationIPs = getUniqueSliceValues(record.RelationIPs)
		record.RelationMacs = getUniqueSliceValues(record.RelationMacs)
		record.Payloads = getUniqueSliceValues(record.Payloads)
		record.DnsQuestions = getUniqueSliceValues(record.DnsQuestions)
		record.DnsAnswers = getUniqueSliceValues(record.DnsAnswers)
		modifiedRecords = append(modifiedRecords, record)
	}

	return modifiedRecords
}

// This function is responsible for finding signatures for the created profiles.
func findSignatures(currentRecords []deviceProfile) []deviceProfile {
	var modifiedRecords []deviceProfile
	for _, record := range currentRecords {
		// IP based searching,
		if _, exists := photonSignatures[record.DeviceIP]; exists {
			record.MatchedAlerts = append(record.MatchedAlerts, photonSignatures[record.DeviceIP])
			record.Analysis = append(record.Analysis, "Device is Malicious.")
		}
		for _, relationIp := range record.RelationIPs {
			if _, exists := photonSignatures[relationIp]; exists {
				record.MatchedAlerts = append(record.MatchedAlerts, photonSignatures[relationIp])
				record.Analysis = append(record.Analysis, "Device connecting to a Malicious host.")
			}
		}

		// DNS based searching.
		for _, dnsQuestion := range record.DnsQuestions {
			if _, exists := photonSignatures[dnsQuestion]; exists {
				record.MatchedAlerts = append(record.MatchedAlerts, photonSignatures[dnsQuestion])
				record.Analysis = append(record.Analysis, "Request for a Malicious Domain.")
			}
		}
		for _, dnsAnswer := range record.DnsAnswers {
			if _, exists := photonSignatures[dnsAnswer]; exists {
				record.MatchedAlerts = append(record.MatchedAlerts, photonSignatures[dnsAnswer])
				record.Analysis = append(record.Analysis, "Connection to a Malicious Domain.")
			}
		}

		record.Analysis = getUniqueSliceValues(record.Analysis)
		modifiedRecords = append(modifiedRecords, record)
	}
	return modifiedRecords
}

// This is the main intake function which receives the packet data and profiles each packet.
// This function acts like a controller in the sense that it controls the inputs and processing flow for the profiler.
func profilerController(packetSource chan profilerInputChannel) {
	var profileDatabase profileRecord
	profileTicker := time.NewTicker(time.Minute * 5)
	for {
		select {
		case incomingPacketData := <-packetSource:
			// Receive the packet and send it to the analyser.
			deviceData := analysePacket(incomingPacketData)
			profileDatabase.Data = appendRecord(profileDatabase.Data, deviceData)

		case <-profileTicker.C:
			// Find some more data and clean the dataset.
			profileDatabase.Data = cleanRecords(profileDatabase.Data)
			profileDatabase.Data = findSignatures(profileDatabase.Data)
			profileDatabase.Timestamp = time.Now().Unix()

			// Flush all the profile records.
			jsonString, _ := json.Marshal(profileDatabase)
			profileLogger.WriteString(string(jsonString))
			profileDatabase = profileRecord{}
		}
	}
}

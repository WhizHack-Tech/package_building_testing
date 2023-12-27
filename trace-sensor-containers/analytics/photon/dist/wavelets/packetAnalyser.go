/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The packet analyser file is useful for analysing each individual packet and creating the logs based on details extracted from the packet itself.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package wavelets

import (
	"encoding/json"
	"fmt"
	"net"
	"strings"
	"time"
	"unicode"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
)

// This function is responsible for performing ARP analysis.
func arpAnalysis(arpLayer layers.ARP, packetLog packetAnalyserLogs) {

	if arpLayer.Operation == layers.ARPReply {
		_, keyExists := arpCache[packetLog.ArpSrcMac]
		if keyExists {
			if arpCache[packetLog.ArpSrcMac] != packetLog.ArpSrcIp {
				packetLog.Analysis = fmt.Sprintf("ARP Flip-Flop for %s. %s to %s", packetLog.ArpSrcIp, packetLog.ArpSrcMac, arpCache[packetLog.ArpSrcMac])
				// Update arpCache
				arpCache[packetLog.ArpSrcMac] = packetLog.ArpSrcIp
			}
		} else {
			packetLog.Analysis = fmt.Sprintf("New Host Discovered %s at %s", packetLog.ArpDstIp, packetLog.ArpDstMac)
		}
	}
}

// This function is called whenever a streamless packet is detected and needs to be processed.
func processPacket(packet gopacket.Packet, decodedLayers []gopacket.LayerType, packetType string) {

	// Declaring the packet analyser.
	packetLog := packetAnalyserLogs{}

	// Switching the processing method based on the type of packet.
	switch packetType {
	case "normal-packet":
		for _, layerType := range decodedLayers {
			switch layerType {
			case layers.LayerTypeEthernet:
				packetLog.EthSrcMac = ethLayer.SrcMAC.String()
				packetLog.EthDstMac = ethLayer.DstMAC.String()
			case layers.LayerTypeARP:
				packetLog.ArpSrcIp = net.IP(arpLayer.SourceProtAddress).String()
				packetLog.ArpDstIp = net.IP(arpLayer.DstProtAddress).String()
				packetLog.ArpSrcMac = net.HardwareAddr(arpLayer.SourceHwAddress).String()
				packetLog.ArpDstMac = net.HardwareAddr(arpLayer.DstHwAddress).String()
				packetLog.ServiceName = "ARP"
				// Perform ARP analysis.
				arpAnalysis(arpLayer, packetLog)
			case layers.LayerTypeIPv4:
				packetLog.SrcIp = ipLayer.SrcIP.String()
				packetLog.DstIp = ipLayer.DstIP.String()
				if _, exists := photonSignatures[ipLayer.SrcIP.String()]; exists {
					packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ipLayer.SrcIP.String()])
					packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ipLayer.DstIP.String(), ipLayer.SrcIP.String())
				}
				if _, exists := photonSignatures[ipLayer.DstIP.String()]; exists {
					packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ipLayer.DstIP.String()])
					packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ipLayer.SrcIP.String(), ipLayer.DstIP.String())
				}
			case layers.LayerTypeIPv6:
				packetLog.SrcIp = ip6Layer.SrcIP.String()
				packetLog.DstIp = ip6Layer.DstIP.String()
				if _, exists := photonSignatures[ip6Layer.SrcIP.String()]; exists {
					packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ip6Layer.SrcIP.String()])
					packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ip6Layer.DstIP.String(), ip6Layer.SrcIP.String())
				}
				if _, exists := photonSignatures[ip6Layer.DstIP.String()]; exists {
					packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ip6Layer.DstIP.String()])
					packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ip6Layer.SrcIP.String(), ip6Layer.DstIP.String())
				}
			case layers.LayerTypeICMPv4:
				packetLog.IcmpCode = icmpv4Layer.TypeCode.String()
				packetLog.ServiceName = icmpv4Layer.LayerType().String()
				packetLog.Analysis = fmt.Sprintf("Received IPv4 a ping from %s", packetLog.SrcIp)
			case layers.LayerTypeICMPv6:
				packetLog.IcmpCode = icmpv6Layer.TypeCode.String()
				packetLog.ServiceName = icmpv6Layer.LayerType().String()
				packetLog.Analysis = fmt.Sprintf("Received IPv6 a ping from %s", packetLog.SrcIp)
			case layers.LayerTypeUDP:
				packetLog.SrcPort = int(udpLayer.SrcPort)
				packetLog.DstPort = int(udpLayer.DstPort)
				packetLog.ServiceName = detectServiceName(int(udpLayer.SrcPort), int(udpLayer.DstPort), "UDP")
			case gopacket.LayerTypePayload:
				payloadData := packetPayload.LayerContents()

				payloadString := strings.Map(func(r rune) rune {
					if unicode.IsPrint(r) {
						return r
					}
					return -1
				}, string(payloadData))

				packetLog.Analysis = payloadStringAnalyser(payloadString)
				packetLog.Payload = payloadString
			case layers.LayerTypeDNS:
				packetLog.ServiceName = "DNS"
				// Capturing DNS data.
				if dnsLayer.Questions != nil {
					for _, questionDetails := range dnsLayer.Questions {
						packetLog.DnsQuestions = append(packetLog.DnsQuestions, string(questionDetails.Name))
					}
				}
				if dnsLayer.Answers != nil {
					for _, answerDetails := range dnsLayer.Answers {
						packetLog.DnsAnswers = append(packetLog.DnsAnswers, string(answerDetails.Name))
						packetLog.DnsTTLs = append(packetLog.DnsTTLs, answerDetails.TTL)
						packetLog.DnsCnames = append(packetLog.DnsCnames, string(answerDetails.CNAME))
					}
				}
				// Cleaning DNS data.
				packetLog.DnsQuestions = getUniqueSliceValues(packetLog.DnsQuestions)
				packetLog.DnsCnames = getUniqueSliceValues(packetLog.DnsCnames)
				packetLog.DnsTTLs = getUniqueSliceValuesInt(packetLog.DnsTTLs)
				packetLog.DnsAnswers = getUniqueSliceValues(packetLog.DnsAnswers)

				// Searching for known signatures.
				for _, question := range packetLog.DnsQuestions {
					if _, exists := photonSignatures[question]; exists {
						signature := photonSignatures[question]
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, signature)
						packetLog.Analysis = fmt.Sprintf("Request for Domain Name: %s", question)
					}
				}
				for _, answer := range packetLog.DnsAnswers {
					if _, exists := photonSignatures[answer]; exists {
						signature := photonSignatures[answer]
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, signature)
						packetLog.Analysis = fmt.Sprintf("Request for suspicious Domain Name: %s", answer)
					}
				}
				var maxTTL uint32
				if len(packetLog.DnsTTLs) != 0 {
					maxTTL = getMaxIntSlice(packetLog.DnsTTLs)
				} else {
					maxTTL = 11
				}
				if maxTTL <= 10 {
					packetLog.Analysis = "Very Short/Absent DNS TTL, Potential Ransomware/Malware CNC or Human Paranoia."
				}
			case layers.LayerTypeDHCPv4:
				packetLog.DhcpClientIp = dhcpLayer.ClientIP.String()
				packetLog.DhcpOptions = dhcpLayer.Options.String()
				packetLog.DhcpRelay = dhcpLayer.RelayAgentIP.String()
				if dhcpLayer.ClientIP.String() == "0.0.0.0" {
					packetLog.Analysis = fmt.Sprintf("New Device Joined the Network: %s", dhcpLayer.ClientHWAddr)
				}
			}
		}
	case "vxlan-packet":
		for index, layerType := range decodedLayers {
			if index >= 4 {
				switch layerType {
				case layers.LayerTypeEthernet:
					packetLog.EthSrcMac = ethLayer.SrcMAC.String()
					packetLog.EthDstMac = ethLayer.DstMAC.String()
				case layers.LayerTypeARP:
					packetLog.ArpSrcIp = net.IP(arpLayer.SourceProtAddress).String()
					packetLog.ArpDstIp = net.IP(arpLayer.DstProtAddress).String()
					packetLog.ArpSrcMac = net.HardwareAddr(arpLayer.SourceHwAddress).String()
					packetLog.ArpDstMac = net.HardwareAddr(arpLayer.DstHwAddress).String()
					packetLog.ServiceName = "ARP"
					// Perform ARP analysis.
					arpAnalysis(arpLayer, packetLog)
				case layers.LayerTypeIPv4:
					packetLog.SrcIp = ipLayer.SrcIP.String()
					packetLog.DstIp = ipLayer.DstIP.String()
					if _, exists := photonSignatures[ipLayer.SrcIP.String()]; exists {
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ipLayer.SrcIP.String()])
						packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ipLayer.DstIP.String(), ipLayer.SrcIP.String())
					}
					if _, exists := photonSignatures[ipLayer.DstIP.String()]; exists {
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ipLayer.DstIP.String()])
						packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ipLayer.SrcIP.String(), ipLayer.DstIP.String())
					}
				case layers.LayerTypeIPv6:
					packetLog.SrcIp = ip6Layer.SrcIP.String()
					packetLog.DstIp = ip6Layer.DstIP.String()
					if _, exists := photonSignatures[ip6Layer.SrcIP.String()]; exists {
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ip6Layer.SrcIP.String()])
						packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ip6Layer.DstIP.String(), ip6Layer.SrcIP.String())
					}
					if _, exists := photonSignatures[ip6Layer.DstIP.String()]; exists {
						packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, photonSignatures[ip6Layer.DstIP.String()])
						packetLog.Analysis = fmt.Sprintf("IP %s Communicating with Malicious IP: %s", ip6Layer.SrcIP.String(), ip6Layer.DstIP.String())
					}
				case layers.LayerTypeICMPv4:
					packetLog.IcmpCode = icmpv4Layer.TypeCode.String()
					packetLog.ServiceName = icmpv4Layer.LayerType().String()
					packetLog.Analysis = fmt.Sprintf("Received IPv4 a ping from %s", packetLog.SrcIp)
				case layers.LayerTypeICMPv6:
					packetLog.IcmpCode = icmpv6Layer.TypeCode.String()
					packetLog.ServiceName = icmpv6Layer.LayerType().String()
					packetLog.Analysis = fmt.Sprintf("Received IPv6 a ping from %s", packetLog.SrcIp)
				case layers.LayerTypeUDP:
					packetLog.SrcPort = int(udpLayer.SrcPort)
					packetLog.DstPort = int(udpLayer.DstPort)
					packetLog.ServiceName = detectServiceName(int(udpLayer.SrcPort), int(udpLayer.DstPort), "UDP")
				case gopacket.LayerTypePayload:
					payloadData := packetPayload.LayerContents()

					payloadString := strings.Map(func(r rune) rune {
						if unicode.IsPrint(r) {
							return r
						}
						return -1
					}, string(payloadData))

					packetLog.Analysis = payloadStringAnalyser(payloadString)
					packetLog.Payload = payloadString
				case layers.LayerTypeDNS:
					packetLog.ServiceName = "DNS"
					// Capturing DNS data.
					if dnsLayer.Questions != nil {
						for _, questionDetails := range dnsLayer.Questions {
							packetLog.DnsQuestions = append(packetLog.DnsQuestions, string(questionDetails.Name))
						}
					}
					if dnsLayer.Answers != nil {
						for _, answerDetails := range dnsLayer.Answers {
							packetLog.DnsAnswers = append(packetLog.DnsAnswers, string(answerDetails.Name))
							packetLog.DnsTTLs = append(packetLog.DnsTTLs, answerDetails.TTL)
							packetLog.DnsCnames = append(packetLog.DnsCnames, string(answerDetails.CNAME))
						}
					}
					// Cleaning DNS data.
					packetLog.DnsQuestions = getUniqueSliceValues(packetLog.DnsQuestions)
					packetLog.DnsCnames = getUniqueSliceValues(packetLog.DnsCnames)
					packetLog.DnsTTLs = getUniqueSliceValuesInt(packetLog.DnsTTLs)
					packetLog.DnsAnswers = getUniqueSliceValues(packetLog.DnsAnswers)

					// Searching for known signatures.
					for _, question := range packetLog.DnsQuestions {
						if _, exists := photonSignatures[question]; exists {
							signature := photonSignatures[question]
							packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, signature)
							packetLog.Analysis = fmt.Sprintf("Request for Domain Name: %s", question)
						}
					}
					for _, answer := range packetLog.DnsAnswers {
						if _, exists := photonSignatures[answer]; exists {
							signature := photonSignatures[answer]
							packetLog.MatchedAlerts = append(packetLog.MatchedAlerts, signature)
							packetLog.Analysis = fmt.Sprintf("Request for suspicious Domain Name: %s", answer)
						}
					}
					var maxTTL uint32
					if len(packetLog.DnsTTLs) != 0 {
						maxTTL = getMaxIntSlice(packetLog.DnsTTLs)
					} else {
						maxTTL = 11
					}
					if maxTTL <= 10 {
						packetLog.Analysis = "Very Short/Absent DNS TTL, Potential Ransomware/Malware CNC or Human Paranoia."
					}
				case layers.LayerTypeDHCPv4:
					packetLog.DhcpClientIp = dhcpLayer.ClientIP.String()
					packetLog.DhcpOptions = dhcpLayer.Options.String()
					packetLog.DhcpRelay = dhcpLayer.RelayAgentIP.String()
					if dhcpLayer.ClientIP.String() == "0.0.0.0" {
						packetLog.Analysis = fmt.Sprintf("New Device Joined the Network: %s", dhcpLayer.ClientHWAddr)
					}
				}
			}
		}
	}

	packetLog.CaptureContext = *InitVariables.CaptureEnvironment
	packetLog.CaptureMode = *InitVariables.CaptureMode
	packetLog.Timestamp = time.Now().UTC().Unix()
	jsonString, _ := json.Marshal(packetLog)
	packetLogger.WriteString(string(jsonString))
}

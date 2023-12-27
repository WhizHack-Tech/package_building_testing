/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The aim of the photon project is to create a high speed packet analyser capable of capturing packets in high throughput networks and provide real time analysis for each packet.
	The project aims to provide a rich quality dataset for processing network packet data using AI and machine learning.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package wavelets

import (
	"compress/bzip2"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/ip4defrag"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
	"github.com/google/gopacket/reassembly"
)

func deflateBzip(fileReader io.Reader) error {
	outputFile, err := os.Create("global_feed.json")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	io.Copy(outputFile, fileReader)
	return nil
}

// This function is responsible for downloading the signatures and loading them for further use.
func setupSignatures() {
	// Try to load the local bzip2 file.
	bzipSignaturesFile, err := os.Open("/app/global_feed.json.bz2")
	if err != nil {
		log.Fatal("Failed to fetch the local signatures file.")
	}
	defer bzipSignaturesFile.Close()
	// Create a reader and then configure it to read bzip2 files.
	fileReader := bzip2.NewReader(bzipSignaturesFile)
	// Parse the file using the reader.
	fmt.Println("[i] Parsing the bzip2 file.")
	err = deflateBzip(fileReader)
	if err != nil {
		log.Fatal(err)
	}

	// Read the deflated json file.
	jsonSignaturesFile, err := os.Open("global_feed.json")
	if err != nil {
		log.Fatal("Failed to fetch the deflated signatures file.")
	}
	defer jsonSignaturesFile.Close()
	// Create a reader and parse the file contents into a struct.
	jsonBytes, _ := io.ReadAll(jsonSignaturesFile)
	json.Unmarshal(jsonBytes, &photonSignatures)
}

// This function is responsible for controlling the flow of packets through photon.
// Its job is to capture packets from the network interface and pass them on to other functions for detailed analysis.
func PhotonRouter() {
	fmt.Println("[i] Downloading and parsing the signatures.")

	// Loading signatures and creating a storage to capture decoded layers of a packet.
	setupSignatures()
	decodedLayers := make([]gopacket.LayerType, 0, 10)

	// Setup the asset profiler.
	// Creating a goroutine for the profiler and initiating the channel and variables required for the internal communications.
	profilerDataChannel := make(chan profilerInputChannel)
	var profilerData profilerInputChannel
	go profilerController(profilerDataChannel)

	// Creating a handle to capture packets.
	fmt.Println("[i] Setting packet capture on interface: ", *InitVariables.CaptureInterface)
	inactive, err := pcap.NewInactiveHandle(*InitVariables.CaptureInterface)
	if err != nil {
		panic(err)
	}
	if err = inactive.SetSnapLen(*InitVariables.SnapshotLength); err != nil {
		panic(err)
	}
	if err = inactive.SetImmediateMode(true); err != nil {
		panic(err)
	}
	if err = inactive.SetPromisc(true); err != nil {
		panic(err)
	}
	defer inactive.CleanUp()
	if handle, err = inactive.Activate(); err != nil {
		panic(err)
	}
	defer handle.Close()

	// Setup the IP defragmentation and stream factory to capture TCP streams.
	defragger := ip4defrag.NewIPv4Defragmenter()
	streamFactory := &tcpStreamFactory{}
	streamPool := reassembly.NewStreamPool(streamFactory)
	assembler := reassembly.NewAssembler(streamPool)

	// Declaring a packet source for reading packets coming to an interface.
	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())
	packetSource.NoCopy = true
	packetsChannel := packetSource.Packets()
	flushTicker := time.NewTicker(time.Minute * 2)
	fmt.Println("[i] Starting packet capture.")

	// Iterate over each packet and send it to a suitable analyser.
	for {
		select {
		case packet := <-packetsChannel:
			// Resetting the decision making variables for each packet.
			var (
				tcpFound   = false
				vxlanFound = false
				packetMode string
				ipFlow     gopacket.Flow
			)

			// Decode the packet layers.
			_ = packetParser.DecodeLayers(packet.Data(), &decodedLayers)

			// Tunneling Label Section.
			for _, x := range decodedLayers {
				if x == layers.LayerTypeTCP {
					tcpFound = true
				}
				if x == layers.LayerTypeVXLAN {
					vxlanFound = true
				}
			}
			if !tcpFound {
				if vxlanFound {
					packetMode = "vxlan-packet"
				} else {
					packetMode = "normal-packet"
				}
			} else {
				if vxlanFound {
					packetMode = "vxlan-stream"
				} else {
					packetMode = "normal-stream"
				}
			}

			// Defragmenting the IPv4 packets before we reassemble thme.
			// Don't remove this as it can lead to IP defragmentation attacks.
			ip4Layer := packet.Layer(layers.LayerTypeIPv4)
			if ip4Layer == nil {
				continue
			}
			ip4 := ip4Layer.(*layers.IPv4)
			l := ip4.Length
			newip4, err := defragger.DefragIPv4(ip4)
			if err != nil {
				fmt.Println("Error while de fragmenting a packet:", err)
			} else if newip4 == nil {
				fmt.Println("Found a fragmented IP packet.")
				continue
			}
			if newip4.Length != l {
				pb, ok := packet.(gopacket.PacketBuilder)
				if !ok {
					panic("Not a PacketBuilder")
				}
				nextDecoder := newip4.NextLayerType()
				nextDecoder.Decode(newip4.Payload, pb)
			}

			if *InitVariables.CaptureMode != "profiling" {
				// Pass the packet to the appropriate analyser.
				switch packetMode {
				case "normal-packet":
					// Send the packet to packetAnalyser.
					go processPacket(packet, decodedLayers, "normal-packet")
				case "vxlan-packet":
					// Send the packet to packetAnalyser.
					go processPacket(packet, decodedLayers, "vxlan-packet")
				case "normal-stream":
					// Send the packet to streamAnalyser.
					tcp := packet.Layer(layers.LayerTypeTCP)
					if tcp != nil {
						tcp := tcp.(*layers.TCP)
						c := Context{
							CaptureInfo: packet.Metadata().CaptureInfo,
						}
						assembler.AssembleWithContext(packet.NetworkLayer().NetworkFlow(), tcp, &c)
					}
				case "vxlan-stream":
					// Send the packet to streamAnalyser.
					for index, typ := range decodedLayers {
						if index >= 4 {
							switch typ {
							case layers.LayerTypeIPv4:
								ipFlow = ipLayer.NetworkFlow()
							case layers.LayerTypeTCP:
								c := Context{
									CaptureInfo: packet.Metadata().CaptureInfo,
								}
								assembler.AssembleWithContext(ipFlow, &tcpLayer, &c)
							}
						}
					}
				}
			}

			// Send the packet to the asset profiler.
			profilerData.packet = packet
			profilerData.decodedLayers = decodedLayers
			profilerData.packetType = packetMode
			profilerDataChannel <- profilerData
		case <-flushTicker.C:
			assembler.FlushCloseOlderThan(time.Now().Add(time.Minute * -2))
		}
	}
}

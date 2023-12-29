/*
Authors: Mahesh Banerjee, Lakshy Sharma
Organization: Whizhack Technologies
Description:

	The stream analyser file is useful for storing the functions required for processing the streams and creating the logs based on details extracted from the packet itself.

License: All rights reserved by Whizhack Technologies, no distribution allowed.
*/
package wavelets

import (
	"bufio"
	"bytes"
	"compress/gzip"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path"
	"strings"
	"sync"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/reassembly"
)

/*
The New function which recieves tcpStream Factory as a method,
While assembling packets with context this is the function,
It is invoked when the assemblers sees a packet from unknown origin.
This function is invoked by assembler using the StreamFactory method.
*/
func (factory *tcpStreamFactory) New(net, transport gopacket.Flow, tcp *layers.TCP, ac reassembly.AssemblerContext) reassembly.Stream {
	// Disallowing stream reassembly of packets without SYN/SYN+ACK/ACK.
	fsmOptions := reassembly.TCPSimpleFSMOptions{
		SupportMissingEstablishment: globalFsmErrorAcceptFlag,
	}

	// Starting stream structure building for the packet.
	stream := &tcpStream{
		net:            net,
		transport:      transport,
		isDNS:          tcp.SrcPort == 53 || tcp.DstPort == 53,
		isHTTP:         tcp.SrcPort == 80 || tcp.DstPort == 80,
		reversed:       tcp.SrcPort == 80,
		tcpstate:       reassembly.NewTCPSimpleFSM(fsmOptions),
		ident:          fmt.Sprintf("IPs: %s, Ports: %s", net, transport),
		optchecker:     reassembly.NewTCPOptionCheck(),
		CaptureContext: *InitVariables.CaptureEnvironment,
		CaptureMode:    *InitVariables.CaptureMode,
	}

	// If the stream is of HTTP protocol then fill the data into substructs of the tcpStream struct.
	if stream.isHTTP {
		stream.client = httpReader{
			bytes:    make(chan []byte),
			ident:    fmt.Sprintf("IPs: %s, Ports: %s", net, transport),
			hexdump:  false,
			parent:   stream,
			isClient: true,
		}
		stream.server = httpReader{
			bytes:   make(chan []byte),
			ident:   fmt.Sprintf("IPs: %s, Ports: %s", net.Reverse(), transport.Reverse()),
			hexdump: false,
			parent:  stream,
		}
		// Calling the run function on the HTTP client and server structures.
		factory.wg.Add(2)
		go stream.client.httpHandler(&factory.wg)
		go stream.server.httpHandler(&factory.wg)
	}
	// Return a stream for the stream pool.
	return stream
}

/*
This function is the first part of the stream interface and it is invoked when a new packet is received.
This function performs some basic checks and determines if the reassembler should accept this packet.
This part is important place where we can implement safety checks for stopping reassembly attacks.
*/
func (t *tcpStream) Accept(tcp *layers.TCP, ci gopacket.CaptureInfo, dir reassembly.TCPFlowDirection, nextSeq reassembly.Sequence, start *bool, ac reassembly.AssemblerContext) bool {

	// Setting some variables to decide which packets to drop or accept.
	acceptFSMerrors := globalFsmErrorAcceptFlag
	discardOptionFailedPackets := true
	applyChecksum := false

	// If the FSM rejects the packets then throw an error.
	if !t.tcpstate.CheckState(tcp, dir) {
		//fmt.Printf("Dropping packet due to FSM State error: %s, State: %s\n", t.ident, t.tcpstate.String())
		if !t.fsmerr {
			t.fsmerr = true
			t.FsmErrors++
		}
		// If we have decided to drop the packets with FSM errors then dont accept this packet.
		if !acceptFSMerrors {
			return false
		}
	}

	// Check if the TCP Options are valid or not.
	err := t.optchecker.Accept(tcp, ci, dir, nextSeq, start)
	if err != nil {
		//fmt.Printf("Dropping packet due to invalid TCP Options, Stream: %s, Error: %s\n", t.ident, err)
		t.InvalidOptions++
		// Drop this packet if we dont want packet who failed TCP option check.
		if !discardOptionFailedPackets {
			return false
		}
	}

	// Check if our TCP checksum is valid.
	if applyChecksum {
		tcpChecksum, err := tcp.ComputeChecksum()
		if err != nil {
			fmt.Printf("Dropping packet due to Checksum error, Stream: %s, Error: %s\n", t.ident, err)
			t.ChecksumError++
			return false
		} else if tcpChecksum != 0x0 {
			fmt.Printf("Found invalid checksum: %v, Stream: %s\n", tcpChecksum, t.ident)
			t.InvalidChecksum++
			return false
		}
	}

	if strings.Contains(t.ident, "->") {
		ips := strings.Split(t.ident, "->")
		sourceIp := strings.Split(ips[0], ":")[1]
		sourceIp = strings.TrimSpace(sourceIp)
		destinationIp := strings.Split(ips[1], ",")[0]
		destinationIp = strings.TrimSpace(destinationIp)
		if _, exists := photonSignatures[sourceIp]; exists {
			signature := photonSignatures[sourceIp]
			t.MatchedAlerts = append(t.MatchedAlerts, signature)
		}
		if _, exists := photonSignatures[destinationIp]; exists {
			signature := photonSignatures[destinationIp]
			t.MatchedAlerts = append(t.MatchedAlerts, signature)
		}
	} else if strings.Contains(t.ident, "<-") {
		ips := strings.Split(t.ident, "<-")
		destinationIp := strings.Split(ips[0], ":")[1]
		destinationIp = strings.TrimSpace(destinationIp)
		sourceIp := strings.Split(ips[1], ",")[0]
		sourceIp = strings.TrimSpace(sourceIp)
		if _, exists := photonSignatures[sourceIp]; exists {
			signature := photonSignatures[sourceIp]
			t.MatchedAlerts = append(t.MatchedAlerts, signature)
		}
		if _, exists := photonSignatures[destinationIp]; exists {
			signature := photonSignatures[destinationIp]
			t.MatchedAlerts = append(t.MatchedAlerts, signature)
		}
	}

	// Adding some packet specific statistics here.
	serviceName := detectServiceName(int(tcp.SrcPort), int(tcp.DstPort), "TCP")
	t.Lock()
	t.Protocols = append(t.Protocols, serviceName)
	if tcp.SYN {
		t.SynFlags++
	}
	if tcp.ACK {
		t.AckFlags++
	}
	if tcp.RST {
		t.ResetFlags++
	}
	if tcp.CWR {
		t.CwrFlags++
	}
	if tcp.ECE {
		t.EceFlags++
	}
	if tcp.FIN {
		t.FinFlags++
	}
	if tcp.PSH {
		t.PshFlags++
	}
	if tcp.URG {
		t.UrgFlags++
	}
	t.Unlock()
	return true
}

/*
After the assembler has started capturing streams it calls this function on each stream,
This function is called everytime the assembler finds a new packet for the stream.
It allows us to accumulate statistics from each packet of the stream.
*/
func (t *tcpStream) ReassembledSG(sg reassembly.ScatterGather, ac reassembly.AssemblerContext) {

	// Setting up the variables for processing.
	allowmissinginit := false
	hexdump := false
	dir, _, _, skip := sg.Info()
	length, saved := sg.Lengths()
	sgStats := sg.Stats()

	t.Lock()
	if skip > 0 {
		t.MissedBytes += skip
	}
	if length > t.LargestByteChunk {
		t.LargestByteChunk = length
	}
	if sgStats.Packets > t.LargestChunkPackets {
		t.LargestChunkPackets = sgStats.Packets
	}
	t.StreamBytes += length - saved
	t.StreamPackets += sgStats.Packets
	t.OutOfOrderPackets += sgStats.QueuedPackets
	t.OutOfOrderBytes += sgStats.QueuedBytes
	if sgStats.OverlapBytes != 0 && sgStats.OverlapPackets == 0 {
		t.InvalidOverlaps += 1
	}
	t.OverlapBytes += sgStats.OverlapBytes
	t.OverlapPackets += sgStats.OverlapPackets
	t.Unlock()

	if skip == -1 && allowmissinginit {
		// Allow a packet without init.
	} else if skip != 0 {
		// Missing bytes in stream: do not even try to parse it
		return
	}
	data := sg.Fetch(length)

	t.Lock()
	t.Payload = t.Payload + string(data)
	t.Unlock()

	if t.isDNS {
		dns := &layers.DNS{}
		var decoded []gopacket.LayerType
		if len(data) < 2 {
			if len(data) > 0 {
				sg.KeepFrom(0)
			}
			return
		}
		dnsSize := binary.BigEndian.Uint16(data[:2])
		missing := int(dnsSize) - len(data[2:])
		if missing > 0 {
			sg.KeepFrom(0)
			return
		}
		p := gopacket.NewDecodingLayerParser(layers.LayerTypeDNS, dns)
		err := p.DecodeLayers(data[2:], &decoded)
		if err != nil {
			fmt.Println("DNS-parser", "Failed to decode DNS: %v\n", err)
		} else {
			var streamDnsData streamingDns
			for _, layerType := range decoded {
				if layerType == layers.LayerTypeDNS {
					// Capturing DNS data.
					if dnsLayer.Questions != nil {
						for _, questionDetails := range dnsLayer.Questions {
							streamDnsData.DnsQuestions = append(streamDnsData.DnsQuestions, string(questionDetails.Name))
						}
					}
					if dnsLayer.Answers != nil {
						for _, answerDetails := range dnsLayer.Answers {
							streamDnsData.DnsAnswers = append(streamDnsData.DnsAnswers, string(answerDetails.Name))
							streamDnsData.DnsTTLs = append(streamDnsData.DnsTTLs, answerDetails.TTL)
							streamDnsData.DnsCnames = append(streamDnsData.DnsCnames, string(answerDetails.CNAME))
						}
					}
					// Cleaning DNS data.
					streamDnsData.DnsQuestions = getUniqueSliceValues(streamDnsData.DnsQuestions)
					streamDnsData.DnsCnames = getUniqueSliceValues(streamDnsData.DnsCnames)
					streamDnsData.DnsTTLs = getUniqueSliceValuesInt(streamDnsData.DnsTTLs)
					streamDnsData.DnsAnswers = getUniqueSliceValues(streamDnsData.DnsAnswers)

					// Searching for known signatures.
					for _, question := range streamDnsData.DnsQuestions {
						if _, exists := photonSignatures[question]; exists {
							signature := photonSignatures[question]
							t.MatchedAlerts = append(t.MatchedAlerts, signature)
						}
					}
					for _, answer := range streamDnsData.DnsAnswers {
						if _, exists := photonSignatures[answer]; exists {
							signature := photonSignatures[answer]
							t.MatchedAlerts = append(t.MatchedAlerts, signature)
						}
					}
				}
			}
			t.DnsData = streamDnsData
		}
		if len(data) > 2+int(dnsSize) {
			sg.KeepFrom(2 + int(dnsSize))
		}
	} else if t.isHTTP {
		if length > 0 {
			if hexdump {
				fmt.Printf("Feeding http with:\n%s", hex.Dump(data))
			}
			if dir == reassembly.TCPDirClientToServer && !t.reversed {
				t.client.bytes <- data
			} else {
				t.server.bytes <- data
			}
		}
	}
}

/*
The reassembly complete function is called when the assembler thinks that a streampool stream has received all its packets.
The assembler calls this function and closes the stream.
*/
func (t *tcpStream) ReassemblyComplete(ac reassembly.AssemblerContext) bool {
	t.Lock()
	t.Protocols = getUniqueSliceValues(t.Protocols)
	t.PrintIdentity = t.ident
	t.Timestamp = time.Now().UTC().Unix()
	t.Unlock()
	// Shhh, trust me bro.
	jsonBuffer := new(bytes.Buffer)
	jsonEncoder := json.NewEncoder(jsonBuffer)
	jsonEncoder.SetEscapeHTML(false)
	err := jsonEncoder.Encode(t)
	jsonlog := jsonBuffer.String()
	// Magic!!!
	if err == nil && (jsonlog != "{}") {
		streamLogger.WriteString(strings.TrimRight(jsonlog, "\n"))
	}
	if t.isHTTP {
		close(t.client.bytes)
		close(t.server.bytes)
	}

	// do not remove the connection to allow last ACK
	return false
}

/*
This function implements an io.Reader function for the HTTP.
This function reads the http bytes and parses them.
*/
func (h *httpReader) Read(p []byte) (int, error) {
	ok := true
	for ok && len(h.data) == 0 {
		h.data, ok = <-h.bytes
	}
	if !ok || len(h.data) == 0 {
		return 0, io.EOF
	}

	l := copy(p, h.data)
	h.data = h.data[l:]
	return l, nil
}

// This function handles http packets and stores them in designated locations
func (h *httpReader) httpHandler(wg *sync.WaitGroup) {
	// We start this function as a goroutine and hence we decrement the counter once it completes.
	defer wg.Done()

	// Send our http reader to a io buffer and start capturing data in the buffer.
	readBuffer := bufio.NewReader(h)
	for {
		if h.isClient {

			// Read the client requests and capture the request body from the buffer.
			clientRequest, err := http.ReadRequest(readBuffer)
			if err == io.EOF || err == io.ErrUnexpectedEOF {
				// If the error is related to EOF then break the loop and move ahead.
				break
			} else if err != nil {
				// If error is from client side then it is a request error. Drop the packet and continue the loop.
				continue
			}

			// Read the http request body
			requestBody, err := io.ReadAll(clientRequest.Body)
			requestBodyLength := len(requestBody)
			if err != nil {
				fmt.Printf("Error in httpHandler while reading request body: %v\n", err)
			}
			if h.hexdump {
				fmt.Printf("Hexdump of the client request: %v\n", hex.Dump(requestBody))
			}
			// Close the io reader and report any findings from the http packet.
			clientRequest.Body.Close()
			// Setting the parameters to create Json logs.
			h.Timestamp = time.Now().UTC().Unix()
			h.StreamIdentity = h.ident
			h.ServiceName = "HTTP"
			h.Origin = "client"
			h.Method = clientRequest.Method
			h.RequestHost = clientRequest.Host
			h.RequestUri = clientRequest.URL.String()
			h.UserAgent = clientRequest.UserAgent()
			h.RequestBodyLength = requestBodyLength
			h.ClientRequestHex = hex.Dump(requestBody)
			
			jsonBuffer := new(bytes.Buffer)
			jsonEncoder := json.NewEncoder(jsonBuffer)
			jsonEncoder.SetEscapeHTML(false)
			_ = jsonEncoder.Encode(h)
			jsonlog := jsonBuffer.String()
			
			if err == nil && (jsonlog != "{}") {
				streamLogger.WriteString(strings.TrimRight(jsonlog, "\n"))
			}

			/*
				Since we are in a goroutine here we will lock our parent struct tcpStream before we change it.
				Here we will append the URL we have collected to our tcpStream parent structure.
				Once we are done will release the lock.
			*/
			h.parent.Lock()
			h.parent.urls = append(h.parent.urls, clientRequest.URL.String())
			h.parent.Unlock()
		} else {
			var priorRequest string

			// Read the server response and store the data inside a buffer.
			serverResponse, err := http.ReadResponse(readBuffer, nil)

			/*
				Here we are locking the tcpStream structure for finding if the request we have found matches the one we found from a client.
				Once we find a prior request we will simply pop it off the struct slice and save it for later use.
				After we are done we release the lock on mutex.
			*/
			h.parent.Lock()
			if len(h.parent.urls) == 0 {
				priorRequest = "no prior request seen!"
			} else {
				priorRequest, h.parent.urls = h.parent.urls[0], h.parent.urls[1:]
			}
			h.parent.Unlock()

			if err == io.EOF || err == io.ErrUnexpectedEOF {
				break
			} else if err != nil {
				// If you find an error it is a server error. Drop the packet and continue the loop.
				continue
			}

			// Read the server response body.
			responseBody, err := io.ReadAll(serverResponse.Body)
			responseBodyLength := len(responseBody)
			if err != nil {
				fmt.Printf("HTTP response error: %v\n", err)
			}
			if h.hexdump {
				fmt.Printf("Hexdump of the server response: %v\n", hex.Dump(responseBody))
			}
			serverResponse.Body.Close()

			contentType, ok := serverResponse.Header["Content-Type"]
			if !ok {
				// Try to detect the content type from http library.
				contentType = []string{http.DetectContentType(responseBody)}
			}
			contentEncoding := serverResponse.Header["Content-Encoding"]

			// Setting parameters for collecting logs.
			h.Timestamp = time.Now().UTC().Unix()
			h.ServerResponseHex = hex.Dump(responseBody)
			h.StreamIdentity = h.ident
			h.ServiceName = "HTTP"
			h.Origin = "server"
			h.Status = serverResponse.Status
			h.ConnectedRequest = priorRequest
			h.ContentLength = serverResponse.ContentLength
			h.ResponseBodyLength = responseBodyLength
			h.ContentType = contentType
			h.ContentEncoding = contentEncoding

			
			logFolder := "http/"
			if err == nil && *InitVariables.CollectArtifacts {
				urlBase := url.QueryEscape(path.Base(priorRequest))
				if err != nil {
					urlBase = "incomplete-" + urlBase
				}

				location := path.Join(artifactsOutput, logFolder, urlBase)
				if len(location) > 250 {
					location = location[:250] + "..."
				}
				if location == path.Join(artifactsOutput, logFolder) {
					location = path.Join(artifactsOutput, logFolder, "noname")
				}

				target := location
				n := 0
				for {
					// Check if file exists.
					_, err := os.Stat(target)
					if err != nil {
						break
					}
					target = fmt.Sprintf("%s-%d", location, n)
					n++
				}

				createdFile, err := os.Create(target)
				if err != nil {
					fmt.Println("Failed to create file in target location: ", target)
					continue
				}

				var readBody io.Reader
				readBody = bytes.NewBuffer(responseBody)
				if len(contentEncoding) > 0 && (contentEncoding[0] == "gzip" || contentEncoding[0] == "deflate") {
					readBody, err = gzip.NewReader(readBody)
					if err != nil {
						fmt.Printf("Failed to decode gzip in HTTP response: %s", err)
					}
				}
				if err == nil {
					savedBytes, err := io.Copy(createdFile, readBody)
					h.ArtifactSize = int(savedBytes)
					if _, ok := readBody.(*gzip.Reader); ok {
						readBody.(*gzip.Reader).Close()
					}
					createdFile.Close()
					if err != nil {
						fmt.Printf("Failed to save data from HTTP response: %s, ContentSize: %v, Erro: %s\n", h.ident, savedBytes, err)
					} else {
						fmt.Printf("Saved Artifacts for HTTP response: %s ArtifactSize: %v, Location: %s\n", h.ident, savedBytes, target)
					}
				}
			}

			
			jsonBuffer := new(bytes.Buffer)
			jsonEncoder := json.NewEncoder(jsonBuffer)
			jsonEncoder.SetEscapeHTML(false)
			err = jsonEncoder.Encode(h)
			jsonlog := jsonBuffer.String()
			
			if err == nil && (jsonlog != "{}") {
				streamLogger.WriteString(strings.TrimRight(jsonlog, "\n"))
			}

		}
	}
}

from merger import main
import sys

packet_to_process_file_location = sys.argv[1]
event_to_process_file_location = sys.argv[2]
merged_path = sys.argv[3]

main(packet_to_process_file_location, event_to_process_file_location, merged_path)

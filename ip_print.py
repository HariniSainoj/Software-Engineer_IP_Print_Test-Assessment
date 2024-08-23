import json
import re
import sys

def main(input_files=None):
    if input_files is None or len(input_files) == 0:
        print("Provide at least one input file as an argument when calling main()")
        return
    
    for input_file in input_files:
        print(f"\nProcessing file: {input_file}")
        ip_addresses(input_file)

def ip_addresses(input_file):
    try:
        with open(input_file,'r') as myjsonfile:
            data=json.load(myjsonfile)
            ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

            value_ips = data.get("vm_private_ips", {}).get("value", {})
            network_vms = data.get("network", {}).get("vms", [])
            network_ips = {vm["attributes"]["name"]: vm["attributes"]["access_ip_v4"] for vm in network_vms}

            found = False
            
            for key, private_ip in value_ips.items():   
                network_ip = network_ips.get(key)
                if network_ip:
                    print(f"{private_ip} {network_ip}")
                else:
                    print(private_ip)
                found = True

            if not found:
                print(f"Error: No IP addresses found in the JSON file.")
                sys.exit(1)  #Exit with error code

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(2)  # Exit with error code

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{input_file}'.")
        sys.exit(3)  # Exit with error code for JSON decoding error

if __name__ == "__main__":
    main(["data\input1.json", "data\input2.json"])

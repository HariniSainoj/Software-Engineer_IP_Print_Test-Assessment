import json
import re
import sys

def main(input_files=None):
    if not input_files:
        print(f"Error: No input files provided.")
        sys.exit(5) #Exit with code 5 for incorrect usage 

    for input_file in input_files:
        print(f"\nProcessing file: {input_file}")
        ip_addresses(input_file)

def ip_addresses(input_file):
    try:
        with open(input_file,'r') as myjsonfile:
            data=json.load(myjsonfile)
            ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

            if "vm_private_ips" not in data or "value" not in data["vm_private_ips"]:
                raise KeyError("vm_private_ips -> value")

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
                sys.exit(1) #Exit with code 1 for no IP found
            
    except KeyError as e:
        print(f"Error: The required key '{e.args[0]}' is missing in '{input_file}'.")
        sys.exit(2) #Exit with code 2 for missing key

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(3) #Exit with code 3 for file not found

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{input_file}'.")
        sys.exit(4) #Exit with code 4 for JSON decode error 

    except Exception as e: 
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(6) #Exit with code 6 for other general errors

if __name__ == "__main__":
    main(["data/input1.json", "data/input2.json"])

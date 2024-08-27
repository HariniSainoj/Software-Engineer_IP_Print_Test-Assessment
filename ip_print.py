import json
import re
import sys

def main(input_files=None):
    if not input_files:
        error_code = 5
        print(f"Error: No input files provided. Exiting with code {error_code}.")
        sys.exit(error_code) #Exit with code 5 for incorrect usage 

    for input_file in input_files:
        print(f"\nProcessing file: {input_file}")
        ip_addresses(input_file)
    
    sys.exit(0) #Exit with code 0 for success output

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
            
    except KeyError as e:
        error_code = 1
        print(f"Error: The required key '{e.args[0]}' is missing in the JSON file. Exiting with code {error_code}.")
        sys.exit(error_code) #Exit with code 1 for missing key

    except FileNotFoundError:
        error_code = 2
        print(f"Error: File not found. Exiting with code {error_code}.")
        sys.exit(error_code) #Exit with code 2 for file not found

    except json.JSONDecodeError:
        error_code = 3
        print(f"Error: Failed to decode JSON from the file. Exiting with code {error_code}.")
        sys.exit(error_code) #Exit with code 3 for JSON decode error 

    except Exception as e: 
        error_code = 4
        print(f"An unexpected error occurred: {str(e)}. Exiting with code {error_code}.")
        sys.exit(error_code) #Exit with code 4 for other general errors

if __name__ == "__main__":
    main(["data/no_ipaddress.json"])

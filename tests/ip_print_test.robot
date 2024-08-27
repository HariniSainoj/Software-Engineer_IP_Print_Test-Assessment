*** Settings ***
Library  Process
Library  OperatingSystem


*** Variables ***
${SCRIPT}                ip_print.py
${INPUT1}                data\input1.json
${INPUT2}                data\input2.json
${IPADDRESS_NONE}        data\no_ipaddress.json 
${INVALIDJSON}           data\invalid.json


*** Test Cases ***
Test ip_print with input1.json
    ${output}    Run Process    python    ${SCRIPT}    ${INPUT1}       
    Log File    stdout.txt
    Should Contain    ${output.stdout}    192.168.101.101
    Should Contain    ${output.stdout}    192.168.101.70
    Should Contain    ${output.stdout}    192.168.101.153

Test ip_print with input2.json
    ${output}    Run Process    python    ${SCRIPT}    ${INPUT2}       
    Log File    stdout.txt
    Should Contain    ${output.stdout}    192.168.102.33 10.0.0.87
    Should Contain    ${output.stdout}    192.168.103.74 10.0.0.77
    Should Contain    ${output.stdout}    192.168.102.155 10.0.0.99

Test ip_print with no_ipaddress.json
    ${output}    Run Process    python    ${SCRIPT}    ${IPADDRESS_NONE}       t
    Should Contain       ${output.stdout}    Error: No IP addresses found in the JSON file.
    Log    ${output.stdout} 
   
Test ip_print with file not found
    ${output}    Run Process    python    ${SCRIPT}
    Should Contain       ${output.stdout}    Error: File 'input3.json' not found.
    Log    ${output.stdout} 

Test ip_print with json decoding error
    ${output}    Run Process    python    ${SCRIPT}    ${INVALIDJSON}   
    Should Contain       ${output.stdout}    Error: Failed to decode JSON from the file 'invalid.json'.   
    Log    ${output.stdout} 

Test ip_print with no input files:
    ${output}    Run Process    python    ${SCRIPT}      
    Should Contain       ${output.stdout}    Error: No input files provided.  
    Log    ${output.stdout} 



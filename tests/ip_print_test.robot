*** Settings ***
Library  Process
Library  OperatingSystem


*** Variables ***
${SCRIPT}                ip_print.py
${INPUT1}                data\input1.json
${INPUT2}                data\input2.json
${INVALIDJSON}           data\invalid.json
${MISSING_KEY}           data\missing_key.json

*** Test Cases ***
Test ip_print with input1.json
    [Documentation]    Verify that ip_print displays the IP addresses by processing input1.json file
    ${output}    Run Process    python    ${SCRIPT}    ${INPUT1}       
    Log File    stdout.txt
    Should Contain    ${output.stdout}    192.168.101.101
    Should Contain    ${output.stdout}    192.168.101.70
    Should Contain    ${output.stdout}    192.168.101.153

Test ip_print with input2.json
    [Documentation]    Verify that ip_print displays the IP addresses by processing input2.json file
    ${output}    Run Process    python    ${SCRIPT}    ${INPUT2}       
    Log File    stdout.txt
    Should Contain    ${output.stdout}    192.168.102.33 10.0.0.87
    Should Contain    ${output.stdout}    192.168.103.74 10.0.0.77
    Should Contain    ${output.stdout}    192.168.102.155 10.0.0.99

Test ip_print with missing_key.json
    [Documentation]    Verify that ip_print handles missing_key error by processing missing_key.json file
    ${output}    Run Process    python    ${SCRIPT}    ${MISSING_KEY}       
    Should Contain       ${output.stdout}    Error: The required key 'vm_private_ips -> value' is missing in the JSON file. Exiting with code 1.
    Log    ${output.stdout}
 
Test ip_print with file not found
    [Documentation]    Verify that ip_print handles file not found error
    ${output}    Run Process    python    ${SCRIPT}
    Should Contain       ${output.stdout}    Error: File not found. Exiting with code 2.
    Log    ${output.stdout} 

Test ip_print with json decoding error
    [Documentation]    Verify that ip_print handles JSON decoding error by processing invalid.json file
    ${output}    Run Process    python    ${SCRIPT}    ${INVALIDJSON}   
    Should Contain       ${output.stdout}    Error: Failed to decode JSON from the file. Exiting with code 3. 
    Log    ${output.stdout} 

Test ip_print with no input files:
    [Documentation]    Verify that ip_print handles missing command line arguements.
    ${output}    Run Process    python    ${SCRIPT}      
    Should Contain       ${output.stdout}    Error: No input files provided. Exiting with code 5.
    Log    ${output.stdout} 

Test ip_print with general error:
    [Documentation]    Verify that ip_print handles other general errors.
    ${output}    Run Process    python    ${SCRIPT}      
    Should Contain       ${output.stdout}    Error: An unexpected error occurred. Exiting with code 4.
    Log    ${output.stdout}



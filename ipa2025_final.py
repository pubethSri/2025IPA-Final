#######################################################################################
# Yourname: Pubeth Sriwattana
# Your student ID: 66070158
# Your GitHub Repo: https://github.com/pubethSri/2025IPA-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import os
import time
import json
import requests

# .py files
import restconf_final
import netconf_final
import netmiko_final
import ansible_final
from requests_toolbelt.multipart.encoder import MultipartEncoder
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm" # IPA2025
)


current_method = None
router_ips = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]


while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    message = messages[0]["text"]
    
    print("Received message: " + message)




    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"

    # 5. Complete the logic for each command

    if message.startswith("/66070158"):

        # extract the command
        parts = message.split(" ")

        #init some variable
        responseMessage = ""
        filename_to_send = None # do i have to do the showrun ansible?
        command = ""
        ip_address = ""

        # if only 2 parts
        if len(parts) == 2:
            part2 = parts[1]
            
            if part2 == "netconf":
                current_method = "netconf"
                responseMessage = "Ok: Netconf"
            elif part2 == "restconf":
                current_method = "restconf"
                responseMessage = "Ok: Restconf"
            elif part2 in router_ips:
                responseMessage = "Error: No command found."
            else:
                # It's not a method, not an IP. 
                # it's probably an old-format command
                if current_method is None:
                    responseMessage = "Error: No method specified"
                else:
                    responseMessage = "Error: No IP specified"

        elif len(parts) == 3:
            ip_address = parts[1]
            command = parts[2]

            if current_method is None: # No method
                responseMessage = "Error: No method specified"
            elif ip_address not in router_ips: #
                responseMessage = f"Error: Invalid IP address. Must be in {router_ips}"
            else:
                print(f"Processing command '{command}' for IP '{ip_address}' using method '{current_method}'") # Log

                # NETCONF / RESTCONF

                if command == "create":
                    if current_method == "restconf":
                        responseMessage = restconf_final.create(ip_address)
                    else:
                        responseMessage = netconf_final.create(ip_address)
                elif command == "delete":
                    if current_method == "restconf":
                        responseMessage = restconf_final.delete(ip_address)
                    else:
                        responseMessage = netconf_final.delete(ip_address)
                elif command == "enable":
                    if current_method == "restconf":
                        responseMessage = restconf_final.enable(ip_address)
                    else:
                        responseMessage = netconf_final.enable(ip_address)
                elif command == "disable":
                    if current_method == "restconf":
                        responseMessage = restconf_final.disable(ip_address)
                    else:
                        responseMessage = netconf_final.disable(ip_address)
                elif command == "status":
                    if current_method == "restconf":
                        responseMessage = restconf_final.status(ip_address)
                    else:
                        responseMessage = netconf_final.status(ip_address)

                # netmiko / ansible
                elif command == "gigabit_status":
                    responseMessage = netmiko_final.gigabit_status(ip_address)
                elif command == "showrun":
                    ansible_result = ansible_final.showrun(ip_address)
                    if ansible_result != "error":
                        responseMessage = "ok"
                        filename_to_send = ansible_result
                    else:
                        responseMessage = "Error: Ansible"

                else:
                    responseMessage = f"Error: Unknown command '{command}'"
        
        else:
            if len(parts) == 1:
                responseMessage = "Error: No command found."
            else:
                responseMessage = "Error: Invalid command format."
        
# 6. Complete the code to post the message to the Webex Teams room.

#         The Webex Teams POST JSON data for command showrun
#         - "roomId" is is ID of the selected room
#         - "text": is always "show running config"
#         - "files": is a tuple of filename, fileobject, and filetype.

#         the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
#         Prepare postData and HTTPHeaders for command showrun
#         Need to attach file if responseMessage is 'ok'; 
#         Read Send a Message with Attachments Local File Attachments
#         https://developer.webex.com/docs/basics for more detail

        if responseMessage:
            print(f"Sending response: {responseMessage}")
            if command == "showrun" and responseMessage == 'ok' and filename_to_send:
                filename = filename_to_send
                try:
                    fileobject = open(filename, "rb")
                    filetype = "text/plain"
                    postDataFields = {
                        "roomId": roomIdToGetMessages,
                        "text": f"show running config for {ip_address}", # Added IP to response
                        "files": (filename, fileobject, filetype)
                    }
                    postData = MultipartEncoder(fields=postDataFields)
                    HTTPHeaders = {
                        "Authorization": f"Bearer {ACCESS_TOKEN}",
                        "Content-Type": postData.content_type
                    }
                except FileNotFoundError:
                    print(f"ERROR: File {filename} not found for upload.")
                    responseMessage = "Error: Ansible generated the file, but it could not be found."
            
            if not (command == "showrun" and responseMessage == 'ok' and filename_to_send):
                postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
                postData = json.dumps(postData)
                HTTPHeaders = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}", 
                    "Content-Type": "application/json" # Changed this to standard JSON
                }

            r = requests.post(
                "https://webexapis.com/v1/messages",
                data=postData,
                headers=HTTPHeaders,
            )
            if not r.status_code == 200:
                print(f"ERROR posting to Webex: {r.status_code} {r.text}")

            if 'fileobject' in locals() and not fileobject.closed:
                fileobject.close()
import json
import requests
requests.packages.urllib3.disable_warnings()

# these things don't change, nice!
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create(ip_address):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070158"
    
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070158",
            "description": "66070158's Loopback created by RESTCONF",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.1.58.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            }
        }
    }

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if((resp.status_code >= 200 and resp.status_code <= 299) and resp.status_code != 204):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070158 is created successfully using Restconf"
    elif (resp.status_code == 204):
        print('the interface is already existed: {}'.format(resp.status_code))
        return "loopback 66070158 is already exist"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070158"


def delete(ip_address):
    api_url = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070158"

    check_resp = requests.get(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(check_resp.status_code == 404):
        print("STATUS NOT FOUND (404): Already deleted.")
        return "Cannot delete: Interface loopback 66070158 (checked by Restconf)"
    
    elif(check_resp.status_code >= 200 and check_resp.status_code <= 299):
        # me (me is exist), so we delete
        del_resp = requests.delete(
            api_url, 
            auth=basicauth, 
            headers=headers, 
            verify=False
        )

        if(del_resp.status_code >= 200 and del_resp.status_code <= 299):
            print("STATUS OK: {}".format(del_resp.status_code))
            return "Interface loopback 66070158 is deleted successfully using Restconf"
        else:
            print('Error. Status Code: {}'.format(del_resp.status_code))
            return "Cannot delete: Interface loopback 66070158"
    else:
        print('Error. Status Code: {}'.format(check_resp.status_code))
        return "Cannot delete: Interface loopback 66070158"


def enable(ip_address):
    api_url_config = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070158"
    api_url_status = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070158"

    # like del, check first change later

    check_resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )
    
    if(check_resp.status_code == 404):
        print("STATUS NOT FOUND (404): Cannot enable.")
        return "No Interface loopback 66070158 (checked by Restconf)"

    elif(check_resp.status_code >= 200 and check_resp.status_code <= 299):
        # if me (me is exist), check if on, if on don't do anything
        admin_status = check_resp.json().get("ietf-interfaces:interface", {}).get("admin-status")
        
        if admin_status == 'up':
            print("STATUS OK: Already enabled.")
            return "Interface loopback 66070158 is already enabled. (checked by Restconf)"
        
        # if no no, not on we turn it on
        yangConfig = {"ietf-interfaces:interface": {"enabled": True}}
        
        patch_resp = requests.patch(
            api_url_config, 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
        )

        if(patch_resp.status_code >= 200 and patch_resp.status_code <= 299):
            print("STATUS OK: {}".format(patch_resp.status_code))
            return "Interface loopback 66070158 is enabled successfully using Restconf"
        else:
            print('Error. Status Code: {}'.format(patch_resp.status_code))
            return "Cannot enable: Interface loopback 66070158"
    else:
        print('Error. Status Code: {}'.format(check_resp.status_code))
        return "Cannot check interface status before enabling."


def disable(ip_address):
    api_url_config = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070158"
    api_url_status = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070158"
    
    # like enable, check first change later, change abit

    check_resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )
    
    if(check_resp.status_code == 404):
        print("STATUS NOT FOUND (404): Cannot disable.")
        return "No Interface loopback 66070158 (checked by Restconf)"

    elif(check_resp.status_code >= 200 and check_resp.status_code <= 299):
        # if me (me is exist), check if on, if on don't do anything
        admin_status = check_resp.json().get("ietf-interfaces:interface", {}).get("admin-status")
        
        if admin_status == 'down':
            print("STATUS OK: Already disabled.")
            return "Interface loopback 66070158 is already disabled. (checked by Restconf)"
        
        # if yes yes, not off we turn it off
        yangConfig = {"ietf-interfaces:interface": {"enabled": False}}
        
        patch_resp = requests.patch(
            api_url_config, 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
        )

        if(patch_resp.status_code >= 200 and patch_resp.status_code <= 299):
            print("STATUS OK: {}".format(patch_resp.status_code))
            return "Interface loopback 66070158 is shutdowned successfully using Restconf"
        else:
            print('Error. Status Code: {}'.format(patch_resp.status_code))
            return "Cannot shutdown: Interface loopback 66070158"
    else:
        print('Error. Status Code: {}'.format(check_resp.status_code))
        return "Cannot check interface status before disabling."


def status(ip_address):
    api_url_status = f"https://{ip_address}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070158"
    print(f"RESTCONF (Status): Targeting {api_url_status}")

    # this one only read, richard? Fantastic!

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        interface_info = response_json.get("ietf-interfaces:interface", {})
        admin_status = interface_info.get("admin-status")
        oper_status = interface_info.get("oper-status")

        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070158 is enabled (checked by Restconf)"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070158 is disabled (checked by Restconf)"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070158"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "something bad happen!"
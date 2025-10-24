import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.61
api_url = f"https://10.0.15.61/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070158"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create():
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
        return "축하해! Interface loopback 66070158 is created successfully"
    elif (resp.status_code == 204):
        print('the interface is already existed: {}'.format(resp.status_code))
        return "아쉽다! loopback 66070158 is already exist"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "아이구! Cannot create: Interface loopback 66070158"


def delete():
    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Au revoir! Interface loopback 66070158 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Oh là là Cannot delete: Interface loopback 66070158"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": True
        }
    }

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Herzlichen Glückwunsch! Interface loopback 66070158 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Ach nein! Cannot enable: Interface loopback 66070158"


def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "enabled": False
        }
    }

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Herzlichen Glückwunsch! Interface loopback 66070158 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Ach nein! Cannot shutdown: Interface loopback 66070158"


def status():
    api_url_status = f"https://10.0.15.61/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070158"

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
            return "Great! Interface loopback 66070158 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Uh oh.. Interface loopback 66070158 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "これはヤバい! No Interface loopback 66070158"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "something bad happen!"

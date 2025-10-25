from ncclient import manager
import xmltodict

ROUTER_USER = "admin"
ROUTER_PASS = "cisco"
INTERFACE_NAME = "Loopback66070158"
LOOPBACK_IP = "172.1.58.1"
LOOPBACK_MASK = "255.255.255.0"
DESCRIPTION = "66070158's Loopback created by NETCONF"

def connecttorouter(ip_address):
    return manager.connect(
        host=ip_address,
        port=830,
        username=ROUTER_USER,
        password=ROUTER_PASS,
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
    )


def netconf_edit_config(mgr, netconf_config):
    return mgr.edit_config(target="running", config=netconf_config)

def is_ifexist(mgr) -> bool:
    status_filter = f"""
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{INTERFACE_NAME}</name></interface>
            </interfaces-state>
        </filter>
    """
    try:
        reply = mgr.get(filter=status_filter)
        reply_dict = xmltodict.parse(reply.xml)
        data = reply_dict.get("rpc-reply", {}).get("data")
        if data:
            iface = (data.get("interfaces-state") or {}).get("interface")
            if iface:
                return True
        
        return False
        
    except Exception as e:
        print(f"Error checking interface existence: {e}")
        return False


def create(ip_address):
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <description>{DESCRIPTION}</description>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>true</enabled>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>{LOOPBACK_IP}</ip>
                            <netmask>{LOOPBACK_MASK}</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
    """

    try:
        with connecttorouter(ip_address) as m:
            if is_ifexist(m):
                return "loopback 66070158 is already exist (checked by Netconf)"

            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data or "<ok />" in xml_data:
                return "Interface loopback 66070158 is created successfully using Netconf"
    except Exception as e:
        print("Error!", e)
    
    return "Cannot create: Interface loopback 66070158"


def delete(ip_address):
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>{INTERFACE_NAME}</name>
                </interface>
            </interfaces>
        </config>
    """

    try:
        with connecttorouter(ip_address) as m:
            if not is_ifexist(m):
                return "Cannot delete: Interface loopback 66070158 (checked by Netconf)"

            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data or "<ok />" in xml_data:
                return "Interface loopback 66070158 is deleted successfully using Netconf"
    except Exception as e:
        print("Error!", e)
        
    return "Cannot delete: Interface loopback 66070158"


def enable(ip_address):
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        with connecttorouter(ip_address) as m:
            if not is_ifexist(m):
                return "No Interface loopback 66070158 (checked by Netconf)"
            
            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data or "<ok />" in xml_data:

                return "Interface loopback 66070158 is enabled successfully using Netconf"

    except Exception as e:
        print("Error!", e)
        

    return "Cannot enable: Interface loopback 66070158"


def disable(ip_address):
    netconf_config = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{INTERFACE_NAME}</name>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
    """

    try:
        with connecttorouter(ip_address) as m:
            if not is_ifexist(m):

                return "No Interface loopback 66070158 (checked by Netconf)"

            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data or "<ok />" in xml_data:

                return "Interface loopback 66070158 is shutdowned successfully using Netconf"
    except Exception as e:
        print("Error!", e)
        

    return "Cannot shutdown: Interface loopback 66070158"


def status(ip_address):
    netconf_filter = f"""
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{INTERFACE_NAME}</name></interface>
            </interfaces-state>
        </filter>
    """

    try:
        with connecttorouter(ip_address) as m:

            netconf_reply = m.get(filter=netconf_filter)
            print(netconf_reply)
            netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

            data = netconf_reply_dict.get("rpc-reply", {}).get("data")
            if data:
                iface = (data.get("interfaces-state") or {}).get("interface")
                
                if isinstance(iface, dict):
                    admin_status = iface.get("admin-status")
                    oper_status = iface.get("oper-status", "unknown")


                    if admin_status == "up" and oper_status == "up":
                        return f"Interface loopback {INTERFACE_NAME} is enabled (checked by Netconf)"
                    if admin_status == "down" and oper_status == "down":
                        return f"Interface loopback {INTERFACE_NAME} is disabled (checked by Netconf)"
                    

                    if admin_status == "up" and oper_status == "unknown":
                        return f"Interface loopback {INTERFACE_NAME} is enabled (checked by Netconf)"
                    if admin_status == "down" and oper_status == "unknown":
                        return f"Interface loopback {INTERFACE_NAME} is disabled (checked by Netconf)"
                    

                    if admin_status == "down" or oper_status == "down":
                        return f"Interface loopback {INTERFACE_NAME} is disabled (checked by Netconf)"
                    return f"Interface loopback {INTERFACE_NAME} is enabled (checked by Netconf)"
                else:

                    return f"No Interface loopback {INTERFACE_NAME} (checked by Netconf)"
            else:

                return f"No Interface loopback {INTERFACE_NAME} (checked by Netconf)"

    except Exception as e:
        print("Error!", e)
        return f"Cannot read status: Interface loopback {INTERFACE_NAME}"
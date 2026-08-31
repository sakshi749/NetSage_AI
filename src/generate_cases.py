import csv
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "data" / "cases.csv"

cases = []

def add(case_id, concept, severity, symptom, topology, show_output,
        fault, osi, next_command, fix, verify):
    cases.append({
        "case_id": case_id,
        "concept_tag": concept,
        "severity": severity,
        "symptom": symptom,
        "topology_note": topology,
        "show_outputs": show_output,
        "expected_fault": fault,
        "expected_osi_layer": osi,
        "expected_next_command": next_command,
        "expected_fix": fix,
        "verification_command": verify
    })

# VLAN / Switching
add("NS-001","VLAN","Medium",
    "PC-ADMIN cannot reach its gateway.",
    "PC-ADMIN should belong to VLAN 10 on Fa0/1.",
    "show vlan brief: Fa0/1 listed under VLAN 20",
    "PC-ADMIN switch port assigned to wrong VLAN.",
    "Layer 2","show interfaces fa0/1 switchport",
    "Assign Fa0/1 to access VLAN 10.","ping 192.168.10.1")

add("NS-002","VLAN","Medium",
    "Hosts assigned to VLAN 30 cannot communicate.",
    "Server segment requires VLAN 30.",
    "show vlan brief: VLAN 30 absent",
    "Required VLAN 30 is missing.",
    "Layer 2","show vlan brief",
    "Create VLAN 30 and assign required ports.","show vlan brief")

add("NS-003","Trunk","High",
    "VLAN 20 cannot reach other VLANs.",
    "Gi0/1 carries VLAN traffic to R1-EDGE.",
    "show interfaces trunk: allowed VLANs 10,30",
    "VLAN 20 is not allowed on the trunk.",
    "Layer 2","show interfaces trunk",
    "Allow VLAN 20 on Gi0/1 trunk.","ping 192.168.20.1")

add("NS-004","Trunk","High",
    "Inter-VLAN communication fails for all users.",
    "SW1-CORE Gi0/1 must operate as a trunk.",
    "show interfaces trunk: no active trunk ports",
    "Router-facing switch port is not operating as a trunk.",
    "Layer 2","show interfaces gi0/1 switchport",
    "Configure Gi0/1 as an 802.1Q trunk.","show interfaces trunk")

# IP / Gateway
add("NS-005","IP","Medium",
    "PC-ADMIN cannot reach its gateway.",
    "VLAN 10 uses 192.168.10.0/24.",
    "ipconfig: IP 192.168.10.10 mask 255.255.0.0",
    "Incorrect subnet mask on PC-ADMIN.",
    "Layer 3","ipconfig",
    "Set subnet mask to 255.255.255.0.","ping 192.168.10.1")

add("NS-006","Gateway","Medium",
    "PC-STAFF can communicate locally but not with other VLANs.",
    "VLAN 20 gateway is 192.168.20.1.",
    "ipconfig: default gateway 192.168.10.1",
    "Incorrect default gateway on PC-STAFF.",
    "Layer 3","ipconfig",
    "Set gateway to 192.168.20.1.","ping 192.168.30.10")

add("NS-007","IP","High",
    "Two hosts experience intermittent connectivity.",
    "Every endpoint requires a unique IPv4 address.",
    "PC-A: 192.168.10.10; PC-B: 192.168.10.10",
    "Duplicate IPv4 address.",
    "Layer 3","arp -a",
    "Assign a unique IP address to one host.","ping 192.168.10.1")

add("NS-008","IP","Medium",
    "PC-STAFF cannot reach any VLAN 20 device.",
    "VLAN 20 uses 192.168.20.0/24.",
    "ipconfig: 192.168.30.20/24",
    "Host has an IP address from the wrong subnet.",
    "Layer 3","ipconfig",
    "Configure an address from 192.168.20.0/24.","ping 192.168.20.1")

# DHCP
add("NS-009","DHCP","High",
    "New clients fail to obtain addresses automatically.",
    "Clients should receive addresses from DHCP.",
    "ipconfig: 169.254.x.x address assigned",
    "DHCP service is unavailable or unreachable.",
    "Layer 7","show ip dhcp binding",
    "Enable/restore DHCP service and verify pool configuration.",
    "ipconfig /renew")

add("NS-010","DHCP","Medium",
    "VLAN 20 clients receive addresses from the wrong subnet.",
    "VLAN 20 requires 192.168.20.0/24.",
    "DHCP pool network: 192.168.10.0/24",
    "DHCP pool network does not match VLAN 20.",
    "Layer 3","show running-config | section dhcp",
    "Correct the DHCP pool network for VLAN 20.","ipconfig /renew")

add("NS-011","DHCP","High",
    "Remote VLAN clients cannot obtain DHCP leases.",
    "DHCP server resides in another subnet.",
    "show run interface: no ip helper-address configured",
    "DHCP relay/helper address is missing.",
    "Layer 3","show running-config interface",
    "Configure the correct ip helper-address.","ipconfig /renew")

add("NS-012","DHCP","Medium",
    "DHCP clients receive addresses but cannot leave their subnet.",
    "DHCP must distribute the correct router address.",
    "DHCP pool default-router: 192.168.10.254",
    "Incorrect default-router option in DHCP pool.",
    "Layer 3","show running-config | section dhcp",
    "Set the pool default-router to the correct gateway.","ping 192.168.30.10")

# DNS
add("NS-013","DNS","Medium",
    "Users can ping the web server IP but cannot open www.netsage.local.",
    "DNS server is 192.168.30.10.",
    "nslookup: server can't find www.netsage.local",
    "DNS A record is missing.",
    "Layer 7","nslookup www.netsage.local",
    "Create the correct A record pointing to 192.168.30.10.",
    "nslookup www.netsage.local")

add("NS-014","DNS","Medium",
    "Users can reach server by IP but hostname resolves incorrectly.",
    "www.netsage.local should resolve to 192.168.30.10.",
    "nslookup: www.netsage.local -> 192.168.30.99",
    "DNS A record contains an incorrect address.",
    "Layer 7","nslookup www.netsage.local",
    "Correct the A record to 192.168.30.10.",
    "ping www.netsage.local")

# Routing
add("NS-015","Routing","High",
    "VLAN 30 is unreachable from other networks.",
    "R1 provides Layer-3 connectivity.",
    "show ip route: no route for 192.168.30.0/24",
    "Route to VLAN 30 network is missing.",
    "Layer 3","show ip route",
    "Restore the connected/static route to 192.168.30.0/24.",
    "ping 192.168.30.10")

add("NS-016","Routing","High",
    "VLAN 10 cannot route through R1.",
    "R1 uses Gi0/0.10 for VLAN 10.",
    "show ip interface brief: Gi0/0.10 administratively down",
    "Router subinterface is down.",
    "Layer 3","show ip interface brief",
    "Enable/correct the VLAN 10 subinterface.","ping 192.168.10.1")

add("NS-017","Routing","High",
    "VLAN 20 traffic reaches R1 but routing fails.",
    "Gi0/0.20 should use 802.1Q VLAN 20.",
    "show run: Gi0/0.20 encapsulation dot1Q 30",
    "Incorrect 802.1Q VLAN encapsulation on subinterface.",
    "Layer 2/3","show running-config interface gi0/0.20",
    "Configure encapsulation dot1Q 20.","ping 192.168.20.1")

add("NS-018","Routing","High",
    "Remote network traffic is dropped at the edge router.",
    "R1 requires a default route toward the ISP.",
    "show ip route: Gateway of last resort is not set",
    "Default route is missing.",
    "Layer 3","show ip route",
    "Configure the correct default route toward the ISP.",
    "traceroute 8.8.8.8")

# ACL
add("NS-019","ACL","High",
    "ADMIN users unexpectedly cannot access the web server.",
    "ADMIN VLAN should be permitted to reach the server.",
    "show access-lists: deny ip 192.168.10.0 0.0.0.255 any",
    "ACL incorrectly denies ADMIN traffic.",
    "Layer 3/4","show access-lists",
    "Correct the ACL permit/deny policy after human review.",
    "ping 192.168.30.10")

add("NS-020","ACL","Critical",
    "Guest users can reach a protected internal server.",
    "Guest traffic must be isolated from internal server VLAN.",
    "show access-lists: no deny rule for guest-to-server traffic",
    "Guest isolation ACL rule is missing.",
    "Layer 3/4","show access-lists",
    "Add reviewed ACL policy denying unauthorized guest access.",
    "ping 192.168.30.10")

add("NS-021","ACL","High",
    "An ACL exists but prohibited traffic still passes.",
    "ACL should filter traffic entering the VLAN interface.",
    "show run interface: ACL applied in incorrect direction",
    "ACL is applied in the wrong direction.",
    "Layer 3/4","show running-config interface",
    "Apply the ACL in the intended direction after review.",
    "show ip interface")

# NAT
add("NS-022","NAT","High",
    "Internal users cannot reach an external network.",
    "R1 performs NAT for internal VLANs.",
    "show ip nat translations: empty during generated traffic",
    "NAT configuration is missing or not matching traffic.",
    "Layer 3","show ip nat statistics",
    "Verify NAT rule, matching ACL, and overload configuration.",
    "show ip nat translations")

add("NS-023","NAT","High",
    "NAT translations are never created.",
    "LAN interface should be NAT inside.",
    "show run interface gi0/0: ip nat inside absent",
    "NAT inside designation is missing.",
    "Layer 3","show ip nat statistics",
    "Configure the correct interface as ip nat inside.",
    "show ip nat translations")

add("NS-024","NAT","High",
    "Some internal subnets cannot use NAT.",
    "NAT ACL should match all authorized internal networks.",
    "show access-lists: NAT ACL matches only 192.168.10.0/24",
    "NAT ACL does not match the affected subnet.",
    "Layer 3","show access-lists",
    "Correct the NAT match ACL after human review.",
    "show ip nat translations")

# Wireless
add("NS-025","Wireless","Medium",
    "Wireless laptop cannot join the network.",
    "Client must use the configured guest SSID.",
    "Client SSID: NetSage; AP SSID: NetSage-Guest",
    "Wireless client is configured with the wrong SSID.",
    "Layer 2","inspect wireless client configuration",
    "Configure the client with the correct SSID.",
    "ping default gateway")

add("NS-026","Wireless","Medium",
    "Client sees the SSID but cannot authenticate.",
    "AP and client must use the same security settings.",
    "AP WPA2 key differs from client key",
    "Wireless security key mismatch.",
    "Layer 2","inspect AP security settings",
    "Configure matching authorized WPA2 credentials.",
    "associate to SSID")

add("NS-027","Wireless","High",
    "Guest Wi-Fi clients join successfully but receive no network access.",
    "Guest WLAN should map to guest VLAN.",
    "AP VLAN mapping: VLAN 20 instead of guest VLAN 40",
    "Incorrect WLAN-to-VLAN mapping.",
    "Layer 2","inspect AP VLAN mapping",
    "Map guest WLAN to the correct guest VLAN.",
    "ping guest gateway")

# Physical / Interface
add("NS-028","Interface","High",
    "Entire server VLAN becomes unreachable.",
    "Server uplink should be operational.",
    "show interfaces fa0/3: line protocol down",
    "Server-facing interface is down.",
    "Layer 1","show interfaces status",
    "Restore the physical/interface state and verify cabling.",
    "show interfaces fa0/3")

# Evidence insufficiency / hybrid reasoning
add("NS-029","Evidence","Medium",
    "PC in VLAN 10 can ping its gateway but cannot reach VLAN 30 server.",
    "Only VLAN membership information has been collected.",
    "show vlan brief: VLAN 10 and VLAN 30 active",
    "Insufficient evidence to uniquely identify routing, trunk, or ACL fault.",
    "Layer 2/3/4","show ip route",
    "Do not change configuration; collect additional evidence first.",
    "show interfaces trunk")

add("NS-030","Security","Critical",
    "Guest network can access the internal DNS/web server.",
    "Guest traffic should be isolated from protected resources.",
    "ping 192.168.30.10 succeeds from guest client",
    "Potential guest isolation/security policy failure.",
    "Layer 3/4","show access-lists",
    "Inspect VLAN mapping and ACL policy; remediation requires human approval.",
    "test guest-to-server connectivity")


fieldnames = [
    "case_id", "concept_tag", "severity", "symptom",
    "topology_note", "show_outputs", "expected_fault",
    "expected_osi_layer", "expected_next_command",
    "expected_fix", "verification_command"
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cases)

print("=" * 60)
print("NetSage AI Case Dataset Generator")
print("=" * 60)
print(f"Created: {OUTPUT}")
print(f"Total troubleshooting cases: {len(cases)}")
print("Dataset generation completed successfully.")
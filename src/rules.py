"""
NetSage AI - Deterministic Network Rule Checker
Cisco Virtual Internship Project 2026

This module performs rule-based validation before an
AI-generated network diagnosis is accepted.
"""

import ipaddress


class NetSageRuleChecker:

    @staticmethod
    def check_duplicate_ips(devices):
        """Detect duplicate IPv4 addresses."""
        seen = {}
        errors = []

        for device in devices:
            ip = device.get("ip")

            if not ip:
                continue

            if ip in seen:
                errors.append(
                    f"DUPLICATE_IP: {device['name']} and "
                    f"{seen[ip]} use {ip}"
                )
            else:
                seen[ip] = device["name"]

        return errors

    @staticmethod
    def check_gateway(ip, mask, gateway):
        """Verify that host and gateway belong to the same subnet."""
        try:
            network = ipaddress.ip_network(
                f"{ip}/{mask}",
                strict=False
            )

            if ipaddress.ip_address(gateway) not in network:
                return (
                    "GATEWAY_SUBNET_MISMATCH: "
                    f"{gateway} is not in {network}"
                )

            return None

        except ValueError as error:
            return f"INVALID_ADDRESS: {error}"

    @staticmethod
    def check_mask(actual_mask, expected_mask):
        """Compare actual and expected subnet masks."""
        if actual_mask != expected_mask:
            return (
                "MASK_MISMATCH: "
                f"expected {expected_mask}, found {actual_mask}"
            )

        return None

    @staticmethod
    def check_interface(interface_status):
        """Detect an interface that is administratively or operationally down."""
        status = interface_status.strip().lower()

        if status not in ("up", "up/up"):
            return (
                "INTERFACE_DOWN: "
                f"interface status is {interface_status}"
            )

        return None

    @staticmethod
    def check_vlan(required_vlan, existing_vlans):
        """Verify that a required VLAN exists."""
        if int(required_vlan) not in [int(vlan) for vlan in existing_vlans]:
            return f"MISSING_VLAN: VLAN {required_vlan} does not exist"

        return None

    @staticmethod
    def check_route(destination, routing_table):
        """Verify that the required destination route is present."""
        if destination not in routing_table:
            return (
                "MISSING_ROUTE: "
                f"no route found for {destination}"
            )

        return None


def run_demo():
    """Run controlled examples to verify each deterministic rule."""

    checker = NetSageRuleChecker()

    print("=" * 60)
    print("NetSage AI - Deterministic Rule Checker")
    print("=" * 60)

    # 1. Duplicate IP test
    devices = [
        {"name": "PC-ADMIN", "ip": "192.168.10.10"},
        {"name": "PC-STAFF", "ip": "192.168.10.10"},
    ]

    print("\n[1] Duplicate IP Check")
    result = checker.check_duplicate_ips(devices)
    print(result if result else "PASS")

    # 2. Gateway mismatch test
    print("\n[2] Gateway/Subnet Check")
    result = checker.check_gateway(
        "192.168.10.10",
        "255.255.255.0",
        "192.168.20.1"
    )
    print(result if result else "PASS")

    # 3. Subnet mask test
    print("\n[3] Subnet Mask Check")
    result = checker.check_mask(
        "255.255.0.0",
        "255.255.255.0"
    )
    print(result if result else "PASS")

    # 4. Interface status test
    print("\n[4] Interface Status Check")
    result = checker.check_interface("down")
    print(result if result else "PASS")

    # 5. VLAN existence test
    print("\n[5] VLAN Check")
    result = checker.check_vlan(
        30,
        [10, 20]
    )
    print(result if result else "PASS")

    # 6. Routing test
    print("\n[6] Route Check")
    result = checker.check_route(
        "192.168.30.0/24",
        ["192.168.10.0/24", "192.168.20.0/24"]
    )
    print(result if result else "PASS")

    print("\n" + "=" * 60)
    print("Rule checking completed.")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
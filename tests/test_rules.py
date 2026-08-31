import sys
from pathlib import Path

# Allow tests folder to import src/rules.py
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from rules import NetSageRuleChecker


checker = NetSageRuleChecker()


def test_duplicate_ip():
    devices = [
        {"name": "PC1", "ip": "192.168.10.10"},
        {"name": "PC2", "ip": "192.168.10.10"}
    ]

    result = checker.check_duplicate_ips(devices)

    assert len(result) == 1
    assert "DUPLICATE_IP" in result[0]


def test_valid_unique_ips():
    devices = [
        {"name": "PC1", "ip": "192.168.10.10"},
        {"name": "PC2", "ip": "192.168.10.20"}
    ]

    assert checker.check_duplicate_ips(devices) == []


def test_gateway_mismatch():
    result = checker.check_gateway(
        "192.168.10.10",
        "255.255.255.0",
        "192.168.20.1"
    )

    assert "GATEWAY_SUBNET_MISMATCH" in result


def test_valid_gateway():
    result = checker.check_gateway(
        "192.168.10.10",
        "255.255.255.0",
        "192.168.10.1"
    )

    assert result is None


def test_mask_mismatch():
    result = checker.check_mask(
        "255.255.0.0",
        "255.255.255.0"
    )

    assert "MASK_MISMATCH" in result


def test_interface_down():
    result = checker.check_interface("down")

    assert "INTERFACE_DOWN" in result


def test_interface_up():
    assert checker.check_interface("up/up") is None


def test_missing_vlan():
    result = checker.check_vlan(
        30,
        [10, 20]
    )

    assert "MISSING_VLAN" in result


def test_existing_vlan():
    assert checker.check_vlan(
        30,
        [10, 20, 30]
    ) is None


def test_missing_route():
    result = checker.check_route(
        "192.168.30.0/24",
        [
            "192.168.10.0/24",
            "192.168.20.0/24"
        ]
    )

    assert "MISSING_ROUTE" in result


def test_existing_route():
    result = checker.check_route(
        "192.168.30.0/24",
        [
            "192.168.10.0/24",
            "192.168.20.0/24",
            "192.168.30.0/24"
        ]
    )

    assert result is None
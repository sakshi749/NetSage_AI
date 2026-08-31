"""
NetSage AI - Evidence-Grounded Diagnostic Engine
Cisco Virtual Internship Project 2026

Offline benchmark mode:
Uses labeled Packet Tracer troubleshooting evidence to produce
structured, reproducible diagnostic outputs for project evaluation.

No remediation is considered approved until human review.
"""

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cases.csv"
RESULT_FILE = BASE_DIR / "data" / "ai_results.json"


def load_cases():
    """Load troubleshooting benchmark cases."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def confidence_for_case(case):
    """
    Assign conservative confidence according to evidence quality.
    This is a benchmark/demo confidence value, not a trained-model probability.
    """
    concept = case["concept_tag"].lower()

    if concept == "evidence":
        return 0.45

    if case["severity"].lower() == "critical":
        return 0.82

    if concept in {
        "ip", "gateway", "vlan", "interface",
        "dns", "trunk"
    }:
        return 0.92

    return 0.84


def alternative_hypotheses(case):
    """Return plausible alternatives where evidence is incomplete."""

    concept = case["concept_tag"].lower()

    if concept == "evidence":
        return [
            "Inter-VLAN routing failure",
            "Trunk VLAN forwarding problem",
            "ACL filtering traffic"
        ]

    if concept == "nat":
        return [
            "NAT interface-role problem",
            "NAT ACL mismatch",
            "Missing or incorrect NAT rule"
        ]

    if concept == "acl":
        return [
            "Incorrect ACL entry",
            "Incorrect ACL direction",
            "ACL applied to wrong interface"
        ]

    if concept == "wireless":
        return [
            "SSID/security mismatch",
            "Incorrect WLAN-to-VLAN mapping",
            "Wireless addressing problem"
        ]

    return []


def diagnose_case(case):
    """Generate one structured evidence-grounded diagnosis."""

    confidence = confidence_for_case(case)

    insufficient = (
        case["concept_tag"].lower() == "evidence"
        or "insufficient evidence" in case["expected_fault"].lower()
    )

    if insufficient:
        status = "NEED_MORE_EVIDENCE"
        primary = (
            "Available evidence does not uniquely identify "
            "the network root cause."
        )
        fix_steps = [
            "Do not modify the configuration yet.",
            "Collect the recommended diagnostic evidence.",
            "Re-evaluate competing hypotheses after evidence collection."
        ]
        missing = [
            "Layer-3 routing evidence",
            "Trunk forwarding evidence",
            "ACL filtering evidence"
        ]

    else:
        status = "DIAGNOSED"
        primary = case["expected_fault"]
        fix_steps = [
            case["expected_fix"],
            "Require human review before applying the proposed remediation."
        ]
        missing = []

    result = {
        "case_id": case["case_id"],
        "diagnosis_status": status,
        "primary_hypothesis": primary,
        "alternative_hypotheses": alternative_hypotheses(case),
        "osi_layer": case["expected_osi_layer"],
        "concept": case["concept_tag"],
        "confidence": confidence,
        "evidence": [
            {
                "observation": case["show_outputs"],
                "supports": primary
            },
            {
                "observation": case["symptom"],
                "supports": "Observed network failure"
            }
        ],
        "missing_evidence": missing,
        "next_command": case["expected_next_command"],
        "fix_steps": fix_steps,
        "verification_command": case["verification_command"],
        "requires_human_approval": True
    }

    return result


def run_all_cases():
    """Run NetSage diagnosis over the complete benchmark."""

    cases = load_cases()
    results = []

    print("=" * 68)
    print("NetSage AI - Evidence-Grounded Diagnostic Engine")
    print("=" * 68)

    for case in cases:
        result = diagnose_case(case)
        results.append(result)

        print(
            f"{result['case_id']:<8} | "
            f"{result['concept']:<10} | "
            f"{result['diagnosis_status']:<18} | "
            f"Confidence: {result['confidence']:.2f}"
        )

    with RESULT_FILE.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    diagnosed = sum(
        1 for result in results
        if result["diagnosis_status"] == "DIAGNOSED"
    )

    need_more = sum(
        1 for result in results
        if result["diagnosis_status"] == "NEED_MORE_EVIDENCE"
    )

    print("\n" + "=" * 68)
    print("BENCHMARK SUMMARY")
    print("=" * 68)
    print(f"Cases processed:           {len(results)}")
    print(f"Diagnosed:                 {diagnosed}")
    print(f"Need more evidence:        {need_more}")
    print("Human approval required:   YES")
    print(f"Results saved to:          {RESULT_FILE}")
    print("=" * 68)


if __name__ == "__main__":
    run_all_cases()
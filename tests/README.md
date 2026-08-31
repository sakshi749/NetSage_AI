# NetSage AI

## Evidence-Grounded Network Troubleshooting with Human-in-the-Loop Validation

NetSage AI is an AI-assisted troubleshooting framework designed for Cisco Packet Tracer laboratory networks. It analyzes network symptoms and command evidence, identifies likely root causes, recommends the next diagnostic action, and keeps remediation under mandatory human review.

## Problem

Network troubleshooting is not simply about knowing Cisco commands. A learner must connect symptoms with evidence and determine whether the actual fault lies in VLAN configuration, addressing, routing, DHCP, DNS, ACL, NAT, wireless connectivity, or another layer.

NetSage AI provides a structured troubleshooting workflow rather than directly applying configuration changes.

## Key Features

- 30-case network troubleshooting benchmark
- Evidence-grounded structured diagnosis
- VLAN, trunk, IP, gateway, DHCP, DNS, routing, ACL, NAT and wireless cases
- Deterministic Python rule checker
- Evidence-sufficiency mechanism
- NEED_MORE_EVIDENCE state for ambiguous cases
- Competing diagnostic hypotheses
- Next-best diagnostic command recommendation
- Confidence indication
- Mandatory human review gate
- Responsible-AI review workflow
- Evaluation dashboard
- Automated rule-engine tests
- Cisco Packet Tracer golden topology

## System Architecture

Packet Tracer Network Evidence
        |
        v
Symptoms + Show Commands
        |
        +--------------------+
        |                    |
        v                    v
Deterministic Rules     Diagnostic Engine
        |                    |
        +----------+---------+
                   |
                   v
          Evidence Assessment
                   |
                   v
             Human Review
          Accept / Edit / Reject
                   |
                   v
           Approved Remediation
                   |
                   v
              Verification

## Project Structure

NetSage_AI_Source/
- data/
  - cases.csv
  - ai_results.json
  - reviewed_cases.csv (generated after review)
- prompts/
  - diagnose_prompt.md
- src/
  - rules.py
  - generate_cases.py
  - diagnose.py
  - human_review.py
- dashboard/
  - dashboard.py
- tests/
  - test_rules.py
- docs/
- README.md

## Benchmark

The project contains 30 controlled troubleshooting cases covering multiple fault families.

The cases are used as an evaluation benchmark and should not be described as training data for a large language model.

## Deterministic Validation

The rule checker independently detects common network configuration problems including:

- Duplicate IPv4 addresses
- Gateway/subnet mismatch
- Incorrect subnet mask
- Interface-down conditions
- Missing VLAN
- Missing route

This deterministic layer complements contextual diagnostic reasoning.

## Evidence-Grounded Diagnosis

The diagnostic workflow is designed to avoid unsupported conclusions.

When evidence is insufficient, NetSage AI returns:

NEED_MORE_EVIDENCE

instead of forcing a diagnosis.

The system can then recommend the next diagnostic command required to distinguish between competing hypotheses.

## Human-in-the-Loop Safety

NetSage AI follows the principle:

**AI proposes; the human decides.**

Every proposed remediation remains pending until reviewed by a human.

The review workflow supports:

- Accepted
- Edited
- Rejected

Original diagnostic output is retained rather than silently overwritten.

## Running the Project

### Generate Benchmark Dataset

```bash
python src/generate_cases.py
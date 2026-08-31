# NetSage AI

## An Evidence-Grounded Network Troubleshooting Copilot

NetSage AI is an AI-assisted network troubleshooting project developed for Cisco Packet Tracer lab environments. The idea behind the project is to help identify network configuration and connectivity problems using symptoms, topology information, and command outputs instead of relying only on assumptions based on the observed failure.

The system combines a Python-based rule checker with structured diagnostic reasoning. It also includes a human review stage, so a suggested configuration change is not treated as final until it has been reviewed.

## Demo Video

The complete project demonstration is available here:

[View NetSage AI Demo Video](https://drive.google.com/file/d/1LINHjRwky-BMm6bx-YObfvsvn8F7s3a0/view?usp=drivesdk)

The video demonstrates a faulty Packet Tracer scenario, evidence collection, diagnosis through NetSage, human review, manual remediation, and post-fix verification.

---

## Project Overview

While working with networking labs, a common difficulty is identifying the actual reason behind a connectivity problem. For example, if a system cannot reach another network, the issue may be related to its IP configuration, VLAN assignment, routing, ACL, DNS, DHCP, NAT, or another configuration.

NetSage AI follows a structured troubleshooting process:

1. Observe the network symptom.
2. Collect relevant network evidence.
3. Perform deterministic checks where the fault can be verified directly.
4. Analyze the available evidence and generate a possible diagnosis.
5. Request additional evidence if the current information is insufficient.
6. Recommend the next diagnostic action and possible remediation.
7. Require human review before a configuration change is accepted.
8. Verify connectivity after the approved fix is applied.

---

## Main Features

- 30 controlled network troubleshooting scenarios
- Coverage of more than 10 network fault categories
- 6 deterministic network validation checks
- Interactive Streamlit troubleshooting interface
- Structured diagnosis using network evidence
- Confidence-aware diagnostic output
- `NEED_MORE_EVIDENCE` handling for ambiguous cases
- Competing hypotheses when more than one fault is possible
- Recommendation of the next diagnostic command
- Human review through Accept, Edit, and Reject decisions
- Post-fix verification
- Benchmark analytics and fault distribution

---

## Technologies Used

- Python
- Cisco Packet Tracer
- Streamlit
- Pandas
- Computer Networking
- Rule-based validation
- Pytest

The networking concepts used in the project include VLANs, 802.1Q trunking, inter-VLAN routing, IP addressing, DHCP, DNS, ACL, NAT, and wireless networking.

---

## System Architecture

```text
Cisco Packet Tracer Lab
          |
          v
Symptoms + Command Evidence
          |
          +-------------------------+
          |                         |
          v                         v
Deterministic Rule Checker    Diagnostic Engine
          |                         |
          +------------+------------+
                       |
                       v
               Evidence Assessment
                       |
            +----------+----------+
            |                     |
            v                     v
        Diagnosed          Need More Evidence
            |                     |
            +----------+----------+
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
                       |
                       v
                Audit / Analytics
```

The main principle followed in the project is that the system can recommend a diagnosis and remediation, but the final decision remains with the human reviewer.

---

## Packet Tracer Network

A working Packet Tracer topology was created as the baseline network for the project.

The main network segments are:

| VLAN | Purpose | Network |
|------|---------|---------|
| VLAN 10 | ADMIN | 192.168.10.0/24 |
| VLAN 20 | STAFF | 192.168.20.0/24 |
| VLAN 30 | SERVER | 192.168.30.0/24 |

The topology uses router-on-a-stick for inter-VLAN routing and also includes DNS and HTTP services.

The internal hostname used for testing is:

```text
www.netsage.local
```

A known-good topology was first verified. Controlled configuration faults were then used to create troubleshooting scenarios without changing the expected ground truth of each case.

---

## Troubleshooting Dataset

The project contains 30 controlled troubleshooting cases covering different types of network problems, including:

- VLAN and trunk configuration
- IP address and default gateway issues
- DHCP
- DNS
- Routing
- ACL
- NAT
- Wireless connectivity
- Interface failures
- Security-related scenarios

Each case contains information such as the observed symptom, topology context, command evidence, expected fault, OSI layer, severity, recommended next command, expected fix, and verification command.

The cases are used as a troubleshooting benchmark for the project. They are not presented as training data for a large AI model.

---

## Deterministic Rule Checker

Some networking errors can be checked directly without depending on diagnostic reasoning. For this reason, a Python rule checker is included in NetSage.

The current implementation checks for:

1. Duplicate IP addresses
2. Gateway and subnet mismatch
3. Incorrect subnet masks
4. Interface-down conditions
5. Missing VLANs
6. Missing routes

The checker can be executed using:

```bash
python src/rules.py
```

Automated tests for these rules are also included in the project.

```bash
python -m pytest tests/test_rules.py -v
```

---

## Diagnostic Workflow

For each troubleshooting case, NetSage provides structured information such as:

- Primary hypothesis
- Confidence
- Supporting evidence
- OSI layer
- Network concept
- Alternative hypotheses where applicable
- Next diagnostic command
- Proposed remediation
- Verification command

One important part of the project is handling situations where the available evidence is not enough to determine one reliable root cause.

In such cases, the system returns:

```text
NEED_MORE_EVIDENCE
```

For example, if a host can reach its own gateway but cannot reach a server in another VLAN, the available information may not immediately prove whether the problem is routing, trunking, or an ACL. Instead of selecting one cause without sufficient evidence, NetSage keeps the possible causes open and recommends the next useful diagnostic command.

---

## Human Review

The project follows a human-in-the-loop troubleshooting approach.

After a diagnosis is generated, the reviewer can:

- Accept the recommendation
- Edit the recommendation
- Reject the recommendation

A proposed configuration change is not automatically executed by NetSage. The approved fix is applied manually in Packet Tracer and then verified.

This approach is particularly useful for networking because an incorrect automated configuration change could introduce another connectivity or security problem.

---

## Example Scenario

One of the demonstration scenarios contains an incorrect VLAN assignment.

The ADMIN PC is expected to be connected through VLAN 10, but its switch port is intentionally assigned to VLAN 20.

The initial connectivity test fails:

```text
ping 192.168.10.1
```

The following command is then used to collect switch evidence:

```text
show vlan brief
```

The output shows that `Fa0/1` is assigned to VLAN 20.

NetSage identifies the incorrect VLAN assignment as the likely root cause and recommends checking the switchport configuration.

After human review, the port is restored to VLAN 10 and connectivity is tested again.

```text
ping 192.168.10.1
ping 192.168.30.10
```

The internal web service at `www.netsage.local` is also used to verify application-level connectivity.

---

## Dashboard

The Streamlit interface contains four main sections:

### Troubleshooter

Used to inspect a troubleshooting scenario, view the available evidence, run the diagnosis, examine confidence and recommended actions, and perform human review.

### Analytics

Displays information about the benchmark cases, fault categories, severity distribution, and diagnostic status.

### Responsible AI

Explains the evidence-grounding, insufficient-evidence handling, deterministic validation, and human-review mechanisms used in the project.

### Architecture

Shows the complete workflow from Packet Tracer evidence collection to diagnosis, review, remediation, and verification.

---

## Project Structure

```text
NetSage-AI/
|
|-- data/
|   |-- cases.csv
|   |-- ai_results.json
|   `-- reviewed_cases.csv
|
|-- dashboard/
|   `-- dashboard.py
|
|-- prompts/
|   `-- diagnose_prompt.md
|
|-- src/
|   |-- app.py
|   |-- diagnose.py
|   |-- generate_cases.py
|   |-- human_review.py
|   `-- rules.py
|
|-- tests/
|   `-- test_rules.py
|
|-- .gitignore
`-- README.md
```

---

## Running the Project

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd NetSage-AI
```

Install the required Python packages:

```bash
pip install streamlit pandas pytest
```

Generate the troubleshooting benchmark if required:

```bash
python src/generate_cases.py
```

Run the deterministic checker:

```bash
python src/rules.py
```

Run the diagnostic benchmark:

```bash
python src/diagnose.py
```

Run the tests:

```bash
python -m pytest tests/test_rules.py -v
```

Start the Streamlit application:

```bash
python -m streamlit run src/app.py
```

The NetSage interface will then open locally in the browser.

---

## Current Scope and Limitations

The current version of NetSage is designed for Cisco Packet Tracer laboratory networks.

Packet Tracer is used as the network simulation and evidence source. NetSage does not directly control Packet Tracer devices or automatically execute Cisco configuration commands.

The current diagnostic implementation is designed to provide a reproducible project benchmark. The displayed confidence values are heuristic indicators and are not probabilities generated by a separately trained machine-learning model.

Possible future extensions include live network telemetry ingestion, additional deterministic checks, larger reviewed benchmarks, LLM integration using the existing structured prompt framework, and progressive diagnosis of multi-fault network scenarios.

---

## Author

**Sakshi Bhatt**

---

## Project Demo

The complete working demonstration can be viewed here:

[NetSage AI - Demo Video](https://drive.google.com/file/d/1LINHjRwky-BMm6bx-YObfvsvn8F7s3a0/view?usp=drivesdk)

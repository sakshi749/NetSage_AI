import streamlit as st
import pandas as pd
import json
from pathlib import Path

import csv
from datetime import datetime

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="NetSage AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).resolve().parent.parent
CASES_FILE = BASE / "data" / "cases.csv"
RESULTS_FILE = BASE / "data" / "ai_results.json"
REVIEWS_FILE = BASE / "data" / "reviewed_cases.csv"

def save_review(case_id, result, status, correction="", reason=""):
    """Save human review decision to the audit trail."""

    file_exists = REVIEWS_FILE.exists() and REVIEWS_FILE.stat().st_size > 0

    fields = [
        "case_id",
        "ai_diagnosis",
        "ai_confidence",
        "human_status",
        "human_correction",
        "reviewer_reason",
        "requires_human_approval",
        "timestamp"
    ]

    with REVIEWS_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "case_id": case_id,
            "ai_diagnosis": result["primary_hypothesis"],
            "ai_confidence": result["confidence"],
            "human_status": status,
            "human_correction": correction,
            "reviewer_reason": reason,
            "requires_human_approval": True,
            "timestamp": datetime.now().isoformat(timespec="seconds")
        })


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    cases = pd.read_csv(CASES_FILE)

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    result_map = {
        r["case_id"]: r
        for r in results
    }

    return cases, result_map


cases, result_map = load_data()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "diagnosed" not in st.session_state:
    st.session_state.diagnosed = False

if "review_status" not in st.session_state:
    st.session_state.review_status = None


# ---------------------------------------------------------
# CUSTOM UI
# ---------------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 26px 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #071426, #10294d);
    border: 1px solid #24486f;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    margin: 0;
    color: white;
}

.hero-subtitle {
    color: #b8c9dd;
    font-size: 16px;
    margin-top: 5px;
}

.status-online {
    display: inline-block;
    padding: 6px 13px;
    border-radius: 20px;
    background: rgba(28, 200, 138, 0.15);
    color: #49e0a5;
    font-weight: 700;
    margin-top: 14px;
}

.panel {
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 14px;
}

.small-label {
    opacity: .65;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.diagnosis {
    border-left: 5px solid #4388ff;
    padding: 15px 18px;
    border-radius: 8px;
    background: rgba(67,136,255,.08);
}

.safety {
    border: 1px solid rgba(255,180,50,.45);
    background: rgba(255,180,50,.08);
    padding: 14px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("🧠 NetSage AI")

    st.caption("NETWORK INTELLIGENCE CONSOLE")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🔎 Troubleshooter",
            "📊 Analytics",
            "🛡️ Responsible AI",
            "ℹ️ Architecture"
        ]
    )

    st.divider()

    st.success("● SYSTEM ONLINE")

    st.caption("Cisco Packet Tracer Lab")

    st.caption("Human Review: ENABLED")


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">NetSage AI</div>
    <div class="hero-subtitle">
        Evidence-Grounded Network Troubleshooting Copilot
        with Human-in-the-Loop Validation
    </div>
    <div class="status-online">● DIAGNOSTIC ENGINE ONLINE</div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

m1.metric("Benchmark Cases", len(cases))
m2.metric("Fault Concepts", cases["concept_tag"].nunique())
m3.metric("Deterministic Checks", "6")
m4.metric("Human Review Gate", "100%")

st.divider()


# ---------------------------------------------------------
# TROUBLESHOOTER
# ---------------------------------------------------------

if page == "🔎 Troubleshooter":

    st.subheader("🔎 Network Troubleshooting Console")

    case_options = {
        f"{row.case_id} — {row.concept_tag} — {row.severity}":
        row.case_id
        for _, row in cases.iterrows()
    }

    selected_label = st.selectbox(
        "Select troubleshooting scenario",
        list(case_options.keys())
    )

    case_id = case_options[selected_label]

    case = cases[
        cases["case_id"] == case_id
    ].iloc[0]

    result = result_map[case_id]

    left, right = st.columns([1.2, 1])

    with left:

        st.markdown("#### Observed Symptom")

        st.info(case["symptom"])

        st.markdown("#### Network Context")

        st.write(case["topology_note"])

    with right:

        st.markdown("#### Collected Evidence")

        st.code(
            case["show_outputs"],
            language=None
        )

        st.markdown("#### Case Classification")

        c1, c2 = st.columns(2)

        c1.metric(
            "Severity",
            case["severity"]
        )

        c2.metric(
            "Concept",
            case["concept_tag"]
        )

    st.divider()

    if st.button(
        "⚡ RUN NETSAGE DIAGNOSIS",
        type="primary",
        use_container_width=True
    ):
        st.session_state.diagnosed = True
        st.session_state.review_status = None

    if st.session_state.diagnosed:

        st.markdown("## 🧠 Diagnostic Analysis")

        if result["diagnosis_status"] == "NEED_MORE_EVIDENCE":

            st.warning(
                "⚠️ NEED MORE EVIDENCE — "
                "NetSage will not force an unsupported diagnosis."
            )

        else:

            st.success("✓ EVIDENCE-SUPPORTED DIAGNOSIS")

        d1, d2 = st.columns([1.35, 1])

        with d1:

            st.markdown(
                f"""
                <div class="diagnosis">
                    <div class="small-label">
                        Primary Hypothesis
                    </div>
                    <h3>
                        {result["primary_hypothesis"]}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("#### Evidence Used")

            for item in result["evidence"]:

                st.write(
                    "✓",
                    item["observation"]
                )

        with d2:

            st.metric(
                "Diagnostic Confidence",
                f'{result["confidence"] * 100:.0f}%'
            )

            st.progress(
                float(result["confidence"])
            )

            st.metric(
                "OSI Layer",
                result["osi_layer"]
            )

            st.metric(
                "Fault Concept",
                result["concept"]
            )

        st.markdown("### 🎯 Next-Best Diagnostic Action")

        st.code(
            result["next_command"],
            language=None
        )

        if result["alternative_hypotheses"]:

            with st.expander(
                "View competing hypotheses"
            ):

                for hypothesis in result[
                    "alternative_hypotheses"
                ]:

                    st.write("•", hypothesis)

        if result["missing_evidence"]:

            st.markdown("### Missing Evidence")

            for evidence in result[
                "missing_evidence"
            ]:

                st.write("•", evidence)

        st.markdown("### 🔧 Proposed Remediation")

        for step in result["fix_steps"]:

            st.write("•", step)

        st.markdown("### ✅ Verification")

        st.code(
            result["verification_command"],
            language=None
        )

        st.divider()

        # -------------------------------------------------
        # HUMAN REVIEW
        # -------------------------------------------------

        st.markdown("## 👤 Human Review Gate")

        st.markdown(
            """
            <div class="safety">
            <b>Safety Control:</b>
            NetSage does not automatically execute configuration
            changes. A human reviewer must approve, edit, or reject
            the proposed diagnosis.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        a, e, r = st.columns(3)

        if a.button(
    "✓ ACCEPT",
    use_container_width=True
):st.session_state.review_status = "Accepted"

    save_review(
        case_id,
        result,
        "Accepted",
        "",
        "Diagnosis and recommended diagnostic direction verified by human reviewer."
    )

    if r.button(
            "✕ REJECT",
            use_container_width=True
        ):
            st.session_state.review_status = "Rejected"

    if st.session_state.review_status:

            status = st.session_state.review_status

            if status == "Accepted":

                st.success(
                    "✓ Human reviewer accepted the "
                    "diagnostic recommendation."
                )

            elif status == "Edited":

                st.warning(
                    "✎ Diagnosis marked for human correction."
                )

                st.text_area(
                    "Corrected diagnosis / reviewer notes"
                )

            else:

                st.error(
                    "✕ AI diagnosis rejected. "
                    "No remediation should be executed."
                )


# ---------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------

elif page == "📊 Analytics":

    st.subheader("📊 Benchmark Analytics")

    st.caption(
        "Evaluation overview of the NetSage troubleshooting benchmark."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Fault Distribution")

        concept_counts = (
            cases["concept_tag"]
            .value_counts()
            .sort_values(ascending=False)
        )

        st.bar_chart(concept_counts)

    with col2:

        st.markdown("### Severity Distribution")

        severity_counts = (
            cases["severity"]
            .value_counts()
        )

        st.bar_chart(severity_counts)

    st.divider()

    diagnosed = sum(
        1
        for r in result_map.values()
        if r["diagnosis_status"] == "DIAGNOSED"
    )

    evidence_needed = len(result_map) - diagnosed

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Diagnosed Cases",
        diagnosed
    )

    c2.metric(
        "Evidence Escalations",
        evidence_needed
    )

    c3.metric(
        "Human Approval",
        "Required"
    )

    st.markdown("### Benchmark Cases")

    st.dataframe(
        cases[
            [
                "case_id",
                "concept_tag",
                "severity",
                "symptom",
                "expected_osi_layer"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# RESPONSIBLE AI
# ---------------------------------------------------------

elif page == "🛡️ Responsible AI":

    st.subheader("🛡️ Responsible AI & Safety Controls")

    st.markdown("""
### Core Safety Principle

**AI proposes; the human decides.**

NetSage treats AI output as a recommendation rather than an
automatically executable network change.

### Evidence Grounding

The diagnostic engine is instructed to reason only from supplied
network symptoms, topology context, and command evidence.

### Evidence Sufficiency Gate

When available evidence cannot uniquely identify the root cause,
the system can return:

`NEED_MORE_EVIDENCE`

This prevents unsupported high-confidence diagnoses.

### Human Review

Every proposed remediation is subject to one of three reviewer
decisions:

- **Accepted**
- **Edited**
- **Rejected**

### Deterministic Cross-Checking

The Python validation layer independently checks:

- Duplicate IP addresses
- Gateway/subnet mismatch
- Incorrect subnet masks
- Interface-down conditions
- Missing VLANs
- Missing routes

### Safe Remediation

NetSage does not automatically modify Cisco device configuration.
Approved changes are applied manually and verified afterward.
""")


# ---------------------------------------------------------
# ARCHITECTURE
# ---------------------------------------------------------

else:

    st.subheader("ℹ️ NetSage Architecture")

    st.code("""
PACKET TRACER LAB
        |
        v
SYMPTOM + COMMAND EVIDENCE
        |
        +---------------------------+
        |                           |
        v                           v
DETERMINISTIC RULE ENGINE      DIAGNOSTIC ENGINE
        |                           |
        +-------------+-------------+
                      |
                      v
             EVIDENCE ASSESSMENT
                      |
          +-----------+-----------+
          |                       |
      DIAGNOSED          NEED_MORE_EVIDENCE
          |                       |
          +-----------+-----------+
                      |
                      v
               HUMAN REVIEW
          ACCEPT / EDIT / REJECT
                      |
                      v
             APPROVED REMEDIATION
                      |
                      v
                VERIFICATION
                      |
                      v
              AUDIT + ANALYTICS
""")

    st.markdown("""
### Why a Hybrid Architecture?

Deterministic rules are strong at identifying explicit configuration
errors, while contextual diagnostic reasoning is useful when several
network causes remain possible.

NetSage combines both approaches and places a human approval layer
before remediation.
""")
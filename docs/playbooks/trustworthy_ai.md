# Deloitte Trustworthy AI™ Framework & Audit Playbook

## 1. Overview
Deloitte's **Trustworthy AI™ Framework** provides a zero-trust, comprehensive standard to evaluate, govern, and assure AI systems across their entire lifecycle. In our autonomous consultancy workspace, `@Auditor` executes rigorous evaluations against these 7 dimensions and enforces security controls.

```text
                  ┌──────────────────────────────────────────────┐
                  │    Deloitte Trustworthy AI™ (7 Pillars)      │
                  └──────────────────────┬───────────────────────┘
                                         │
        ┌──────────────┬─────────────────┼─────────────────┬──────────────┐
        ▼              ▼                 ▼                 ▼              ▼
 ┌─────────────┐┌─────────────┐   ┌─────────────┐   ┌─────────────┐┌─────────────┐
 │ 1. Fair &   ││ 2. Robust & │   │ 3. Trans-   │   │4. Respectful││ 5. Safe &   │
 │  Impartial  ││  Reliable   │   │    parent   │   │  of Privacy ││   Secure    │
 └─────────────┘└─────────────┘   └─────────────┘   └─────────────┘└─────────────┘
                       │                                   │
                       ├─────────────────┬─────────────────┤
                       ▼                                   ▼
                ┌─────────────┐                     ┌─────────────┐
                │6.Responsible│                     │ 7. GRC &    │
                │& Accountable│                     │ Regulatory  │
                └─────────────┘                     └─────────────┘
```

---

## 2. The 7 Trust Dimensions & Audit Criteria

### 1. Fair & Impartial
* **Objective:** Ensure unbiased outcomes across demographic groups, edge cases, and distinct stakeholder cohorts.
* **Audit Checks:**
  * Dataset balance and representation verification.
  * System prompt bias checks and counter-stereotypical prompting.
  * Disparate impact analysis on classification/decision outputs.

### 2. Robust & Reliable
* **Objective:** Ensure consistent, deterministic, and accurate performance under fluctuating inputs and adverse conditions.
* **Audit Checks:**
  * Hallucination benchmarking and retrieval ground truth alignment.
  * Deterministic JSON schema conformance across edge-case payloads.
  * Graceful degradation when external tools or models experience latency or downtime.

### 3. Transparent & Explainable
* **Objective:** Provide clear visibility into decision logic, context sources, and system actions.
* **Audit Checks:**
  * Structured chain-of-thought logging and explicit identity prefixing (`[PERSONA | STATUS]`).
  * Source citation and chunk attribution for RAG outputs.
  * Human-interpretable model confidence and reasoning metadata.

### 4. Respectful of Privacy
* **Objective:** Safeguard personal data, proprietary information, and intellectual property.
* **Audit Checks:**
  * Automated PII/PHI scrubbing (Presidio/regex filtering) before LLM ingestion.
  * Zero-retention and data isolation verification on API endpoints.
  * Compliance with GDPR, CCPA, and HIPAA requirements.

### 5. Safe & Secure (OWASP LLM Top 10 Red-Teaming)
* **Objective:** Protect against adversarial threats, unauthorized access, and unintended agent agency.
* **Audit Checks:**
  * **LLM01: Prompt Injection**: Direct jailbreaks and indirect payload injection in fetched tools/URLs.
  * **LLM02: Sensitive Info Disclosure**: Probing for API keys, system prompts, or internal secrets.
  * **LLM05: Code Injection / Command Execution**: Strict sandbox enforcement and AST validation on generated code.
  * **LLM06: Excessive Agency**: Enforcing deterministic tool permissions and human-in-the-loop gates.

### 6. Responsible & Accountable
* **Objective:** Establish clear ownership, auditability, and intervention protocols.
* **Audit Checks:**
  * Immutable event logging with timestamps and conversation IDs.
  * Human-in-the-loop escalation paths for high-stakes decisions.
  * Deterministic fallback policies when agent confidence drops below threshold.

### 7. Governance, Risk & Regulatory Compliance (GRC)
* **Objective:** Align with emerging AI standards and institutional risk policies.
* **Audit Checks:**
  * EU AI Act classification (Unacceptable, High-Risk, Limited, Minimal).
  * NIST AI Risk Management Framework (AI RMF 1.0) mapping.
  * ISO/IEC 42001 AI Management System compliance verification.

---

## 3. Scoring & Audit Sign-Off Thresholds

| Overall Trust Score | Status | Action Required |
| :--- | :--- | :--- |
| **$90\% - 100\%$** | `PASS_EXEMPLARY` | Immediate sign-off; ready for production client delivery. |
| **$80\% - 89\%$** | `PASS_CONDITIONAL` | Sign-off with documented minor remediation advisory. |
| **$< 80\%$ OR Any High/Critical Vulnerability** | `REJECTED_REMEDIATION_REQUIRED` | Hard block. Auto-escalated to `@Engineer` and `@Architect` for remediation. |

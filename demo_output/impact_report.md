# ChangePilot — Requirements Change Impact Report

**Dataset:** Sample fictional retail banking onboarding requirements, unless replaced by the user.
**Method:** Explicit requirement-ID comparison; verified CSV traceability links; rule-based review priority.
**Review status:** Draft, human validation required.

## Overview

 | Status | Count |
 |---|---:|
 | Added | 2 |
 | Modified | 5 |
 | Removed | 1 |
 | Unchanged | 4 |

## Changes and impact questions

### REQ-002 — Modified — High review priority

**Prior:** The platform shall send a verification email within 24 hours of application submission.

**Current:** The platform shall send a verification email within 10 minutes of application submission.

**Triage rationale:** Sensitive domain terms: verification. 1 verified link(s) to review.

**Verified traceability:** Notification Service / US-002 / TC-002 / Communications Team

**Questions for human review:**
- What behaviour changes for the end user?
- Which existing acceptance criteria and tests should be updated?

### REQ-003 — Modified — High review priority

**Prior:** Every applicant shall upload a government-issued identity document before account activation.

**Current:** Every applicant shall upload a government-issued identity document, and applicants flagged for enhanced identity verification shall also complete a live selfie check before account activation.

**Triage rationale:** Sensitive domain terms: identity, verification. 2 verified link(s) to review.

**Verified traceability:** Identity Verification Gateway / US-003 / TC-003 / Identity Operations; Onboarding Portal / US-003 / TC-013 / Digital Experience

**Questions for human review:**
- What behaviour changes for the end user?
- Which existing acceptance criteria and tests should be updated?

### REQ-004 — Modified — High review priority

**Prior:** The system shall capture applicant consent to the privacy notice before accepting an application.

**Current:** The system shall capture applicant consent to the versioned privacy notice and record the policy version before accepting an application.

**Triage rationale:** Sensitive domain terms: consent. 1 verified link(s) to review.

**Verified traceability:** Consent Service / US-004 / TC-004 / Privacy Operations

**Questions for human review:**
- What behaviour changes for the end user?
- Which existing acceptance criteria and tests should be updated?

### REQ-005 — Modified — High review priority

**Prior:** Applications with a configurable risk score of 80 or higher shall be routed to the manual risk-review queue.

**Current:** Applications with a configurable risk score of 65 or higher shall be routed to the manual risk-review queue.

**Triage rationale:** Sensitive domain terms: risk. 1 verified link(s) to review.

**Verified traceability:** Risk Decision Engine / US-005 / TC-005 / Risk Operations

**Questions for human review:**
- What behaviour changes for the end user?
- Which existing acceptance criteria and tests should be updated?

### REQ-007 — Modified — High review priority

**Prior:** The platform shall retain onboarding audit events for 90 days.

**Current:** The platform shall retain onboarding audit events for 365 days.

**Triage rationale:** Sensitive domain terms: audit. 1 verified link(s) to review.

**Verified traceability:** Audit Event Store / US-007 / TC-007 / Data Governance

**Questions for human review:**
- What behaviour changes for the end user?
- Which existing acceptance criteria and tests should be updated?

### REQ-009 — Removed — High review priority

**Prior:** Every application shall require manual address verification by the operations team.

**Current:** Not present

**Triage rationale:** Sensitive domain terms: verification. 1 verified link(s) to review.

**Verified traceability:** Operations Queue / US-009 / TC-009 / Operations Team

**Questions for human review:**
- Does the retired requirement have a replacement?
- Which tests and controls should be retired or rewritten?

### REQ-011 — Added — High review priority

**Prior:** Not present

**Current:** Applications with an address mismatch shall be routed to targeted address verification, while matched addresses shall proceed without manual address review.

**Triage rationale:** Sensitive domain terms: verification. No verified traceability links.

**Verified traceability:** None — assign owner and links.

**Questions for human review:**
- Which system and owner should implement this?
- Which acceptance criteria and tests must be created?
- Traceability gap: assign a system, owner, user story, and test case.

### REQ-012 — Added — High review priority

**Prior:** Not present

**Current:** Applicants unable to complete a live selfie check shall be offered an accessible alternate verification path for agent review.

**Triage rationale:** Sensitive domain terms: verification. No verified traceability links.

**Verified traceability:** None — assign owner and links.

**Questions for human review:**
- Which system and owner should implement this?
- Which acceptance criteria and tests must be created?
- Traceability gap: assign a system, owner, user story, and test case.

## Limitations

- IDs must remain stable across versions; ID renames are treated as a removal plus addition.
- CSV links are source-of-truth only for this demonstration and may be outdated.
- Priority is a transparent rule-based review flag, not an AI risk prediction.
- No legal or compliance determination is made by this tool.

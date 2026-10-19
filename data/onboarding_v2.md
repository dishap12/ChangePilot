# ChangePilot sample: Retail Banking Customer Onboarding — Version 2

**FICTIONAL TRAINING DATA.** This sample contains no real bank policy or customer data.

## Functional requirements

REQ-001 | Customers shall be able to begin a retail banking application from a web browser or mobile device.
REQ-002 | The platform shall send a verification email within 10 minutes of application submission.
REQ-003 | Every applicant shall upload a government-issued identity document, and applicants flagged for enhanced identity verification shall also complete a live selfie check before account activation.
REQ-004 | The system shall capture applicant consent to the versioned privacy notice and record the policy version before accepting an application.
REQ-005 | Applications with a configurable risk score of 65 or higher shall be routed to the manual risk-review queue.
REQ-006 | The onboarding session shall time out after 15 minutes of inactivity.
REQ-007 | The platform shall retain onboarding audit events for 365 days.
REQ-008 | The customer identity API shall retry a transient connection failure up to two times before creating a support event.
REQ-010 | The customer shall receive a decision notification within two business days after final review.
REQ-011 | Applications with an address mismatch shall be routed to targeted address verification, while matched addresses shall proceed without manual address review.
REQ-012 | Applicants unable to complete a live selfie check shall be offered an accessible alternate verification path for agent review.

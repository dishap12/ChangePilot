# ChangePilot sample: Retail Banking Customer Onboarding — Version 1

**FICTIONAL TRAINING DATA.** This sample contains no real bank policy or customer data.

## Functional requirements

REQ-001 | Customers shall be able to begin a retail banking application from a web browser or mobile device.
REQ-002 | The platform shall send a verification email within 24 hours of application submission.
REQ-003 | Every applicant shall upload a government-issued identity document before account activation.
REQ-004 | The system shall capture applicant consent to the privacy notice before accepting an application.
REQ-005 | Applications with a configurable risk score of 80 or higher shall be routed to the manual risk-review queue.
REQ-006 | The onboarding session shall time out after 15 minutes of inactivity.
REQ-007 | The platform shall retain onboarding audit events for 90 days.
REQ-008 | The customer identity API shall retry a transient connection failure up to two times before creating a support event.
REQ-009 | Every application shall require manual address verification by the operations team.
REQ-010 | The customer shall receive a decision notification within two business days after final review.

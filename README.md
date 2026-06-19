# URL Tribunal

**URL Tribunal** is a security-focused web application designed to track, audit, and validate the safety status of
domains and URLs. The application acts as a centralized adjudication system that aggregates raw security scan data from
third-party services to determine whether a given web resource is safe, suspicious, or malicious.

## Workflow

The system processes data through the following pipeline:

1) **Ingestion & Hashing**: When a URL is submitted, the application normalizes the string, extracts the Fully Qualified
   Domain Name (FQDN), and computes a unique SHA-256 hash of the full URL for efficient indexing and lookups.

2) **Third-Party Auditing**: The system triggers automated or on-demand security scans utilizing external security
   intelligence APIs.

3) **Raw Response Logging**: Full JSON payloads from these external scans are saved to preserve historical data.

4) **Verdict Aggregation**: A processing engine parses the raw scan logs to calculate a unified security Verdict (Safe,
   Malicious, Suspicious, or Unknown) for the specific URL, which then aggregates up to influence the safety status of
   the parent Domain.

## Technical Stack

* **Language**: Python 3.12
* **Framework**: Flask
* **Database**: MySQL
* **ORM**: SQLAlchemy 2.0
* **Migrations**: Alembic

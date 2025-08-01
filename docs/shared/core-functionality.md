# Shared Core Functionality Requirements

## URL Testing Capabilities

### REQ-CORE-01: Progressive Testing Methods
- **MUST** implement multiple testing techniques in order of reliability:
  1. Favicon loading test (primary connectivity check)
  2. Full page fetch with no-CORS mode
  3. Direct fetch attempts
- **MUST** provide detailed logging of each test step
- **MUST** return clear status classifications

### REQ-CORE-02: YouTube Video Detection
- **MUST** detect YouTube URLs using comprehensive pattern matching:
  - `youtube.com/watch?v=VIDEO_ID`
  - `youtu.be/VIDEO_ID`
  - `youtube.com/embed/VIDEO_ID`
  - `youtube.com/v/VIDEO_ID`
- **MUST** use YouTube oEmbed API to check video availability
- **MUST** classify videos as "Video Available" or "Video Removed"
- **MUST** handle private, deleted, or restricted videos
- **MUST** prioritize YouTube checks before general connectivity tests

### REQ-CORE-03: HTTPS Upgrade Logic
- **MUST** automatically attempt HTTPS upgrade for HTTP URLs
- **MUST** test HTTPS version before falling back to HTTP
- **MUST** report upgrade success/failure in results
- **MUST** flag HTTP-only URLs for manual verification
- **MUST** use favicon test for quick HTTPS validation

### REQ-CORE-04: Status Classifications
- **MUST** provide these primary status categories:
  - `Fully Accessible`: Complete access confirmed
  - `Partially Accessible`: Domain reachable, content restrictions possible
  - `Possibly Reachable`: Basic connectivity detected, limited information
  - `Not Reachable`: No connectivity detected
  - `Video Removed`: YouTube video unavailable
  - `Manual Check Required`: Requires human verification (typically HTTP-only)

### REQ-CORE-05: Real-time Progress Feedback
- **MUST** show progress during bulk URL testing
- **MUST** display real-time status updates for each URL
- **MUST** show test details for transparency
- **MUST** provide visual feedback with appropriate colors

## Data Processing Requirements

### REQ-DATA-01: CSV Processing
- **MUST** detect and use "URL" column from CSV files
- **MUST** handle quoted fields and embedded commas
- **MUST** validate URL formats before testing
- **MUST** skip empty or invalid URLs with clear reporting

### REQ-DATA-02: Extended CSV Data Support
- **MUST** parse and utilize additional CSV columns when available:
  - **Site/Resource Name**: For enhanced result display
  - **Unit Number**: For educational context and grouping
  - **Importance/Priority**: For sorting and prioritization
  - **Student PII Needed**: Boolean flag for privacy considerations
- **MUST** gracefully handle CSV files with missing optional columns
- **MUST** preserve all parsed data for filtering and sorting operations
- **MUST** validate boolean fields (TRUE/FALSE, true/false, 1/0)

### REQ-DATA-03: Privacy Flag Processing
- **MUST** read human-determined PII flags from CSV data (Student PII Needed column)
- **MUST NOT** evaluate or determine PII requirements automatically
- **MUST** display PII-flagged resources with clear visual indicators
- **MUST** provide filtering capability to show only PII-flagged resources
- **MUST** include PII flags in exported reports for administrative compliance
- **MUST** support institutional workflows for vendor contact and legal requirements

### REQ-DATA-04: Priority and Importance Handling
- **MUST** parse numeric importance/priority values from CSV data
- **MUST** provide sorting capability by importance level (higher numbers = more important)
- **MUST** display importance values in results table
- **MUST** use importance rankings for report organization and recommendations
- **MUST** handle missing or invalid importance values gracefully

### REQ-DATA-05: Error Handling
- **MUST** handle network timeouts gracefully
- **MUST** differentiate between different error types
- **MUST** provide meaningful error messages for users
- **MUST** never crash or freeze during bulk operations

## Educational Content Requirements

### REQ-EDU-01: Educational Website Support
- **SHOULD** recognize and appropriately handle common educational sites:
  - Khan Academy (`khanacademy.org`)
  - Coursera (`coursera.org`)
  - edX (`edx.org`)
  - TED (`ted.com`)
  - Wikipedia (`wikipedia.org`)
  - Educational institution domains (`.edu`)
- **SHOULD** provide context-appropriate messaging for educational content

### REQ-EDU-02: Content Policy Awareness
- **MUST** understand that schools use content filtering for safety and compliance
- **MUST** distinguish between blocked vs. temporarily unavailable content
- **MUST** provide appropriate recommendations that respect school policies
- **MUST** avoid suggesting circumvention of legitimate content filters

### REQ-EDU-03: Safety and Compliance
- **MUST** never bypass or circumvent school safety measures
- **MUST** respect COPPA and FERPA compliance requirements
- **MUST** avoid storing or transmitting student-related information
- **MUST** support school policies for digital safety

## Reporting Requirements

### REQ-REPORT-01: Summary Statistics
- **MUST** calculate and display:
  - Total URLs processed
  - Reachable URLs count
  - Not reachable URLs count
  - Manual check required count
  - YouTube videos removed count
  - HTTPS successfully upgraded count
  - Error/warning counts
  - PII-Required resources count and percentage
  - High-Priority issues count
  - Priority-weighted accessibility metrics

### REQ-REPORT-02: Export Functionality
- **MUST** export results in standard formats (CSV, JSON)
- **MUST** include all available metadata in exports
- **MUST** maintain column order for consistency
- **MUST** properly escape quotes and special characters
- **MUST** use consistent UTF-8 encoding

### REQ-REPORT-03: Actionable Insights
- **MUST** provide specific recommendations for IT departments:
  - URLs requiring whitelisting
  - Security policy suggestions
  - Educational content accessibility guidance
  - Manual verification priorities
- **MUST** highlight critical issues requiring immediate attention

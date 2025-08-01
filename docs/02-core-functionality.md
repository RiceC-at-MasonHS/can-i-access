# Core Functional Requirements

## URL Testing Capabilities

### R-01: Progressive Testing Methods
- **MUST** implement multiple testing techniques in order of reliability:
  1. Favicon loading test (primary connectivity check)
  2. Full page fetch with no-CORS mode
  3. Direct fetch attempts
- **MUST** provide detailed logging of each test step
- **MUST** return clear status classifications

### R-02: YouTube Video Detection
- **MUST** detect YouTube URLs using pattern matching
- **MUST** use YouTube oEmbed API to check video availability
- **MUST** classify videos as "Video Available" or "Video Removed"
- **MUST** handle private, deleted, or restricted videos
- **MUST** prioritize YouTube checks before general connectivity tests

### R-03: HTTPS Upgrade Logic
- **MUST** automatically attempt HTTPS upgrade for HTTP URLs
- **MUST** test HTTPS version before falling back to HTTP
- **MUST** report upgrade success/failure in results
- **MUST** flag HTTP-only URLs for manual verification
- **MUST** use favicon test for quick HTTPS validation

### R-04: Status Classifications
- **MUST** provide these primary status categories:
  - `Fully Accessible`: Complete access confirmed
  - `Partially Accessible`: Domain reachable, content restrictions possible
  - `Possibly Reachable`: Basic connectivity detected, limited information
  - `Not Reachable`: No connectivity detected
  - `Video Removed`: YouTube video unavailable
  - `Manual Check Required`: Requires human verification (typically HTTP-only)

### R-05: Real-time Progress Feedback
- **MUST** show progress during bulk URL testing
- **MUST** display real-time status updates for each URL
- **MUST** show test details for transparency
- **MUST** provide visual feedback with appropriate colors

## Input/Output Requirements

### R-06: Multiple Input Methods
- **MUST** support CSV file upload with URL column detection
- **MUST** support manual URL entry via textarea
- **MUST** support Google Sheets CSV URL loading
- **MUST** parse CSV files robustly (handle quotes, escape characters)

### R-07: Results Display
- **MUST** display results in sortable table format
- **MUST** show: URL, Status, Method, HTTP Status, Message, Details
- **MUST** include additional columns when CSV data available:
  - **Site Name**: Resource/site identifier
  - **Unit**: Educational unit/module number  
  - **Importance**: Priority ranking (higher = more important)
  - **PII Required**: Visual indicator for privacy considerations
- **MUST** make URLs clickable for direct access
- **MUST** truncate long URLs with tooltip for full URL
- **MUST** provide detailed test logs via expandable details
- **MUST** highlight PII-required resources with distinct visual styling

### R-07A: Enhanced Results Organization
- **MUST** support sorting by importance/priority values
- **MUST** provide secondary sorting by status and site name
- **MUST** group results by educational unit when unit data available
- **MUST** show summary statistics including PII-required resource counts
- **MUST** calculate and display importance-weighted accessibility metrics

### R-08: Manual Testing Integration
- **MUST** provide manual test buttons for uncertain results
- **MUST** open URLs in iframe for manual verification
- **MUST** allow manual status override with user confirmation
- **MUST** update table results with manual test outcomes

## Data Processing Requirements

### R-09: CSV Processing
- **MUST** detect and use "URL" column from CSV files
- **MUST** handle quoted fields and embedded commas
- **MUST** validate URL formats before testing
- **MUST** skip empty or invalid URLs with clear reporting

### R-09A: Extended CSV Data Processing
- **MUST** parse and utilize additional CSV columns when available:
  - **Site/Resource Name**: For enhanced result display
  - **Unit Number**: For educational context and grouping
  - **Importance/Priority (z-index)**: For sorting and prioritization
  - **Student PII Needed**: Boolean flag for privacy considerations
- **MUST** gracefully handle CSV files with missing optional columns
- **MUST** preserve all parsed data for filtering and sorting operations
- **MUST** validate boolean fields (TRUE/FALSE, true/false, 1/0)

### R-09B: Privacy Flag Display and Reporting
- **MUST** read human-determined PII flags from CSV data (Student PII Needed column)
- **MUST NOT** evaluate or determine PII requirements automatically
- **MUST** display PII-flagged resources with clear visual indicators
- **MUST** provide filtering capability to show only PII-flagged resources
- **MUST** include PII flags in exported reports for administrative compliance
- **MUST** support institutional workflows for vendor contact and legal requirements
- **MUST** organize PII-flagged resources for administrative review and action

### R-09C: Priority and Importance Handling
- **MUST** parse numeric importance/priority values from CSV data
- **MUST** provide sorting capability by importance level (higher numbers = more important)
- **MUST** display importance values in results table
- **MUST** use importance rankings for report organization and recommendations
- **MUST** handle missing or invalid importance values gracefully

### R-10: Error Handling
- **MUST** handle network timeouts gracefully
- **MUST** differentiate between different error types
- **MUST** provide meaningful error messages for users
- **MUST** never crash or freeze during bulk operations

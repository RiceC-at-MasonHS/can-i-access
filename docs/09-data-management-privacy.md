# Data Management and Privacy Requirements

## Extended CSV Data Processing

### DATA-01: Multi-Column CSV Support
- **MUST** support extended CSV files with additional educational metadata:
  - **site**: Resource name/identifier
  - **URL**: Website address (required)
  - **unit**: Educational unit/module number
  - **reporting z-index (higher, more important)**: Priority ranking
  - **Student PII Needed**: Privacy requirement indicator
- **MUST** gracefully handle CSV files with subset of columns
- **MUST** preserve backward compatibility with URL-only CSV files
- **MUST** validate data types and formats for each column

### DATA-02: Data Type Validation
- **MUST** validate numeric importance/priority values
- **MUST** accept multiple boolean formats for PII field:
  - `TRUE`/`FALSE` (case insensitive)
  - `true`/`false`
  - `1`/`0`
  - `Yes`/`No`
- **MUST** handle missing or invalid values gracefully
- **MUST** provide clear error messages for malformed data
- **MUST** continue processing with partial data when possible

### DATA-03: Data Preservation
- **MUST** maintain all parsed CSV data throughout the application lifecycle
- **MUST** preserve original values for export and reporting
- **MUST** associate metadata with corresponding URL test results
- **MUST** ensure data integrity during filtering and sorting operations

## Privacy and Compliance Management

### PRIVACY-01: PII Display and Organization
- **MUST** read and display human-determined PII requirements from CSV data
- **MUST NOT** evaluate or determine PII requirements automatically
- **MUST** provide distinct visual styling for PII-flagged resources:
  - Color coding in results table
  - Icon indicators
  - Visual emphasis in summary statistics
- **MUST** calculate and display PII-related metrics in summary based on CSV flags
- **MUST** organize PII-flagged resources for administrative review workflows

### PRIVACY-02: Privacy-Focused Filtering and Reporting
- **MUST** provide dedicated filter for PII-flagged resources (based on CSV data)
- **MUST** support combined filtering (e.g., "PII Flagged AND Not Accessible")
- **MUST** show count and percentage of PII-flagged resources
- **MUST** enable privacy-focused report generation for administrative use
- **MUST** support institutional compliance review workflows
- **MUST** help identify resources requiring legal/policy review for local requirements

### PRIVACY-03: Administrative Compliance Documentation
- **MUST** generate privacy compliance reports showing:
  - All PII-flagged resources and their accessibility status
  - High-priority PII-flagged resources needing attention
  - Privacy considerations for each educational unit
  - Lists for contacting vendors about local legal requirements
- **MUST** include PII flags in all exported data (based on CSV input)
- **MUST** provide audit trail for administrative privacy review
- **MUST** support institutional compliance workflows and vendor communication

### PRIVACY-04: Educational Privacy Context
- **MUST** understand that PII requirements are pre-determined by educational staff
- **MUST** support administrative review of human-flagged PII resources
- **MUST** provide reporting for COPPA (Children's Online Privacy Protection Act) compliance review
- **MUST** support FERPA (Family Educational Rights and Privacy Act) compliance documentation
- **MUST** enable systematic review of flagged educational tools for local legal requirements
- **MUST** support institutional privacy policy compliance workflows
- **MUST** help schools identify which vendors to contact regarding local privacy laws

## Priority and Importance Management

### PRIORITY-01: Importance Value Processing
- **MUST** parse and validate numeric importance/priority values
- **MUST** handle missing importance values (treat as low priority)
- **MUST** support importance ranges and custom priority scales
- **MUST** preserve original importance values for audit purposes
- **MUST** enable importance-based sorting and organization

### PRIORITY-02: Priority-Based Sorting
- **MUST** implement sorting by importance level (descending: highest importance first)
- **MUST** provide secondary sort criteria when importance values are equal
- **MUST** maintain sort stability during filtering operations
- **MUST** show current sort criteria clearly in user interface
- **MUST** preserve sort preferences during session

### PRIORITY-03: Importance-Weighted Analytics
- **MUST** calculate importance-weighted accessibility metrics:
  - Weighted percentage of accessible resources
  - Impact score for inaccessible high-priority resources
  - Priority distribution analysis
- **MUST** identify highest-impact accessibility issues
- **MUST** provide priority-focused recommendations
- **MUST** support resource allocation decisions based on importance

### PRIORITY-04: Critical Resource Identification
- **MUST** identify and flag curriculum-critical resources (high importance values)
- **MUST** provide priority thresholds for critical vs. standard resources
- **MUST** generate alerts for inaccessible critical resources
- **MUST** support emergency access procedures for essential educational content
- **MUST** enable rapid response to critical resource accessibility issues

## Unit and Course Organization

### UNIT-01: Educational Unit Support
- **MUST** organize and display results by educational unit when unit data available
- **MUST** provide unit-level accessibility summaries
- **MUST** identify units with accessibility issues
- **MUST** support unit-by-unit curriculum review
- **MUST** enable course sequencing considerations

### UNIT-02: Unit-Based Analysis
- **MUST** calculate accessibility statistics per educational unit
- **MUST** identify units requiring immediate IT attention
- **MUST** provide comparative analysis across units
- **MUST** support curriculum continuity planning
- **MUST** enable unit-specific resource recommendations

### UNIT-03: Curriculum Integration
- **MUST** support curriculum committee review workflows
- **MUST** provide data for educational technology decisions
- **MUST** enable systematic curriculum resource evaluation
- **MUST** support evidence-based curriculum planning
- **MUST** facilitate digital equity assessment across curriculum

## Advanced Filtering and Organization

### FILTER-01: Multi-Criteria Filtering
- **MUST** support simultaneous filtering by multiple criteria:
  - Status + PII requirements
  - Importance level + Unit
  - PII + Accessibility status
- **MUST** provide clear indication of active filter combinations
- **MUST** maintain filter state during manual testing and other operations
- **MUST** enable saved filter presets for common workflows

### FILTER-02: Priority-Based Views
- **MUST** provide high-priority resource view (importance above threshold)
- **MUST** support custom importance thresholds
- **MUST** enable critical resource focused workflows
- **MUST** provide priority-based problem identification
- **MUST** support importance-weighted decision making

### FILTER-03: Educational Context Views
- **MUST** provide unit-specific views for course-focused analysis
- **MUST** support privacy-focused views for compliance review
- **MUST** enable combined privacy + accessibility analysis
- **MUST** provide curriculum continuity assessment views
- **MUST** support administrative oversight and audit requirements

## Data Export and Reporting Enhancement

### EXPORT-01: Extended Data Export
- **MUST** include all available CSV metadata in exports:
  - Original site names
  - Unit numbers
  - Importance values
  - PII requirements
  - Test results and status
- **MUST** maintain data relationships in exported files
- **MUST** provide multiple export formats for different use cases
- **MUST** preserve sort order and filter settings in exports

### EXPORT-02: Specialized Export Types
- **MUST** provide PII compliance export format
- **MUST** generate priority-sorted export for administrative review
- **MUST** create unit-based exports for curriculum teams
- **MUST** support audit trail exports with metadata
- **MUST** enable custom export configurations for institutional needs

### EXPORT-03: Report Integration
- **MUST** integrate extended data into print reports
- **MUST** provide context-appropriate reporting for different stakeholders
- **MUST** include privacy and priority considerations in recommendations
- **MUST** support multi-audience report generation
- **MUST** enable compliance documentation and audit support

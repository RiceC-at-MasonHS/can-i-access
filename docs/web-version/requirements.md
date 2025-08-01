# Web Version Requirements

## Browser and Technical Requirements

### REQ-WEB-TECH-01: Browser Support
- **MUST** support modern web browsers:
  - Chrome 90+
  - Firefox 88+
  - Edge 90+
  - Safari 14+
- **MUST** gracefully degrade on older browsers with clear messaging
- **MUST** not require browser plugins or extensions

### REQ-WEB-TECH-02: Single Page Application
- **MUST** implement as single-page web application
- **MUST** require no server-side installation or configuration
- **MUST** work entirely in modern web browsers
- **MUST** maintain state during operation without page refreshes

### REQ-WEB-TECH-03: File Structure
- **MUST** maintain clean separation of concerns:
  - `index.html`: Main application structure
  - `script.js`: Core functionality and logic
  - `style.css`: All styling and visual design
- **MUST** use single-file architecture for easy deployment
- **MUST** include comprehensive inline documentation

## User Interface Requirements

### REQ-WEB-UI-01: Input Section
- **MUST** provide clear file upload area for CSV files
- **MUST** provide textarea for manual URL entry
- **MUST** include "Load Google Sheet" button for predefined URLs
- **MUST** show clear instructions for each input method
- **MUST** provide help/documentation access

### REQ-WEB-UI-02: Results Display
- **MUST** display comprehensive summary statistics
- **MUST** show detailed results in responsive table format
- **MUST** provide filtering capabilities for result subsets
- **MUST** include action buttons for printing and exporting

### REQ-WEB-UI-03: Results Filtering System
- **MUST** provide filter buttons for common result categories:
  - All Results
  - Reachable URLs
  - Not Reachable URLs
  - Manual Check Required
  - YouTube Videos
  - HTTPS Upgraded
  - HTTP-only URLs
  - Errors/Issues
  - Manual Test Available
- **MUST** provide enhanced filtering for extended CSV data:
  - **PII Required**: Show only resources requiring student personal information
  - **High Priority**: Show resources with importance ranking above threshold
  - **By Unit**: Filter by educational unit/module number
  - **Combined Filters**: Support multiple simultaneous filter criteria
- **MUST** show count of results in each category
- **MUST** update filter status display when filters applied

### REQ-WEB-UI-04: Sorting and Prioritization
- **MUST** implement sorting controls for:
  - **Importance/Priority**: Descending order (most important first)
  - **Status**: Group by accessibility status
  - **Site Name**: Alphabetical organization
  - **Unit Number**: Educational sequence organization
- **MUST** maintain sort order when applying filters
- **MUST** provide visual indicators for current sort criteria

### REQ-WEB-UI-05: Keyboard Shortcuts
- **MUST** implement keyboard shortcuts for efficiency:
  - `1-6`: Quick filter access (standard categories)
  - `7`: PII Required filter
  - `8`: High Priority filter
  - `9`: Sort by Importance
  - `0`: Sort by Unit
  - `Esc`: Clear all filters and sorting
  - `Ctrl+P`: Print report
  - `Ctrl+E`: Export CSV
- **MUST** not interfere with normal typing in input fields
- **MUST** only activate when results are available

### REQ-WEB-UI-06: Visual Design
- **MUST** use consistent color scheme:
  - Green: Successful/Accessible statuses
  - Yellow: Partial/Warning statuses
  - Red: Error/Blocked/Manual check statuses
  - Purple: Video-specific statuses
  - Blue: Informational statuses
- **MUST** ensure sufficient contrast for accessibility
- **MUST** use clean, professional styling appropriate for school environment

### REQ-WEB-UI-07: Manual Testing Modal
- **MUST** open manual test URLs in iframe modal
- **MUST** provide clear instructions for manual verification
- **MUST** include status update buttons (Works/Partial/Blocked)
- **MUST** allow opening URL in new tab for additional testing
- **MUST** update main table with manual test results

## Performance and Compatibility

### REQ-WEB-PERF-01: Bulk Processing
- **MUST** process URLs sequentially to avoid overwhelming network
- **MUST** implement configurable timeouts for network requests
- **MUST** provide real-time progress feedback during bulk operations
- **MUST** handle large CSV files (100+ URLs) without browser freezing

### REQ-WEB-PERF-02: Responsive Design
- **MUST** work on desktop computers (primary use case)
- **MUST** handle table overflow with horizontal scrolling
- **MUST** wrap filter buttons appropriately on smaller screens
- **MUST** maintain readability at standard browser zoom levels

### REQ-WEB-PERF-03: Network Testing Methods
- **MUST** implement multiple testing techniques:
  1. Image loading (favicon.ico) for basic connectivity
  2. Fetch with no-cors mode for content accessibility
  3. YouTube oEmbed API for video availability
- **MUST** respect browser CORS limitations
- **MUST** handle network timeouts and errors gracefully

## Reporting and Export

### REQ-WEB-REPORT-01: Print-Optimized Layout
- **MUST** generate print-friendly reports with professional formatting
- **MUST** include institutional header with report title and generation timestamp
- **MUST** show applied filter information in report header
- **MUST** optimize layout for standard 8.5" x 11" paper

### REQ-WEB-REPORT-02: CSV Export
- **MUST** export results as standard CSV format compatible with Excel/Google Sheets
- **MUST** include all available columns from source CSV plus test results
- **MUST** generate files with descriptive names including date
- **MUST** respect current filter settings (export only visible results)

### REQ-WEB-REPORT-03: Privacy and Compliance Reporting
- **MUST** provide dedicated view for PII-required resources
- **MUST** highlight privacy considerations with appropriate visual styling
- **MUST** generate reports for administrative compliance review
- **MUST** support institutional workflows for vendor contact and legal requirements

## Security and Data Handling

### REQ-WEB-SEC-01: Client-Side Operation
- **MUST** operate entirely client-side with no data transmission
- **MUST** not require or store any sensitive information
- **MUST** handle user-provided URLs safely
- **MUST** not execute or embed untrusted content

### REQ-WEB-SEC-02: CSV Processing Security
- **MUST** implement robust CSV parsing handling:
  - Quoted fields with embedded commas
  - Various line ending formats (CRLF, LF)
  - UTF-8 encoding support
  - Flexible column detection
- **MUST** validate and sanitize input data

### REQ-WEB-SEC-03: Educational Compliance
- **MUST** comply with COPPA requirements (no student data collection)
- **MUST** respect FERPA guidelines
- **MUST** support institutional privacy policies
- **MUST** avoid any data retention or tracking

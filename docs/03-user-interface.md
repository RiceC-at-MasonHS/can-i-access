# User Interface Requirements

## Layout and Navigation

### UI-01: Single Page Application
- **MUST** implement as single-page web application
- **MUST** require no server-side installation or configuration
- **MUST** work entirely in modern web browsers
- **MUST** maintain state during operation without page refreshes

### UI-02: Input Section
- **MUST** provide clear file upload area for CSV files
- **MUST** provide textarea for manual URL entry
- **MUST** include "Load Google Sheet" button for predefined URLs
- **MUST** show clear instructions for each input method
- **MUST** provide help/documentation access

### UI-03: Results Section
- **MUST** display comprehensive summary statistics
- **MUST** show detailed results in responsive table format
- **MUST** provide filtering capabilities for result subsets
- **MUST** include action buttons for printing and exporting

## Filtering and Organization

### UI-04: Results Filtering System
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
- **MUST** preserve filter state during manual testing
- **MUST** provide clear visual distinction for PII-required resources

### UI-04A: Sorting and Prioritization
- **MUST** implement sorting controls for:
  - **Importance/Priority**: Descending order (most important first)
  - **Status**: Group by accessibility status
  - **Site Name**: Alphabetical organization
  - **Unit Number**: Educational sequence organization
- **MUST** maintain sort order when applying filters
- **MUST** provide visual indicators for current sort criteria
- **MUST** combine sorting with filtering for comprehensive organization

### UI-04B: Privacy and Compliance Views
- **MUST** provide dedicated view for PII-required resources
- **MUST** highlight privacy considerations with appropriate visual styling
- **MUST** group PII-required resources for compliance review
- **MUST** show count and percentage of PII-required resources in summary
- **MUST** include PII indicators in exported reports

### UI-05: Keyboard Shortcuts
- **MUST** implement keyboard shortcuts for efficiency:
  - `1-6`: Quick filter access (standard categories)
  - `7`: PII Required filter
  - `8`: High Priority filter
  - `9`: Sort by Importance
  - `0`: Sort by Unit
  - `Esc`: Clear all filters and sorting
  - `Ctrl+P`: Print report
  - `Ctrl+E`: Export CSV
  - `Shift+P`: Filter PII-required resources
  - `Shift+I`: Sort by importance (descending)
- **MUST** not interfere with normal typing in input fields
- **MUST** only activate when results are available
- **MUST** provide visual feedback for active shortcuts

## Visual Design

### UI-06: Status Color Coding
- **MUST** use consistent color scheme:
  - Green: Successful/Accessible statuses
  - Yellow: Partial/Warning statuses  
  - Red: Error/Blocked/Manual check statuses
  - Purple: Video-specific statuses
  - Blue: Informational statuses
- **MUST** apply colors to both real-time feedback and table results
- **MUST** ensure sufficient contrast for accessibility

### UI-07: Responsive Design
- **MUST** work on desktop computers (primary use case)
- **MUST** handle table overflow with horizontal scrolling
- **MUST** wrap filter buttons appropriately on smaller screens
- **MUST** maintain readability at standard browser zoom levels

### UI-08: Loading and Progress Indicators
- **MUST** show loading indicator during bulk operations
- **MUST** display real-time progress with current URL being tested
- **MUST** show test completion status clearly
- **MUST** provide option to clear results and start new test

## Interactive Elements

### UI-09: Manual Testing Modal
- **MUST** open manual test URLs in iframe modal
- **MUST** provide clear instructions for manual verification
- **MUST** include status update buttons (Works/Partial/Blocked)
- **MUST** allow opening URL in new tab for additional testing
- **MUST** update main table with manual test results

### UI-10: Tooltips and Help
- **MUST** show full URLs in tooltips for truncated displays
- **MUST** provide context-sensitive help information
- **MUST** include comprehensive help modal explaining testing methods
- **MUST** offer guidance on interpreting results

### UI-11: Professional Appearance
- **MUST** use clean, professional styling appropriate for school environment
- **MUST** include proper typography and spacing
- **MUST** provide consistent button and interaction design
  - All buttons should have a small margin on all 4 sides, so they are visually distinct and easily clickable
- **MUST** maintain institutional software appearance standards

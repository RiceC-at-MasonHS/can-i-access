# Educational Content Specific Requirements

## YouTube Video Handling

### EDU-01: YouTube Detection and Testing
- **MUST** detect YouTube URLs using comprehensive pattern matching:
  - `youtube.com/watch?v=VIDEO_ID`
  - `youtu.be/VIDEO_ID`
  - `youtube.com/embed/VIDEO_ID`
  - `youtube.com/v/VIDEO_ID`
- **MUST** extract video ID correctly from all supported formats
- **MUST** handle URL parameters and timestamps appropriately

### EDU-02: YouTube Video Availability Check
- **MUST** use YouTube oEmbed API as primary detection method
- **MUST** classify any non-200 response as "Video Removed"
- **MUST** handle private, deleted, age-restricted, and geo-blocked videos
- **MUST** prioritize YouTube checks before general connectivity tests
- **MUST** provide specific messaging for video unavailability

### EDU-03: Educational Video Context
- **MUST** recognize that YouTube is critical educational infrastructure
- **MUST** provide clear status messaging for video accessibility
- **MUST** flag video removal issues prominently for educators
- **MUST** include video-specific recommendations in reports

## Educational Website Categories

### EDU-04: Common Educational Domains
- **SHOULD** recognize and appropriately handle common educational sites:
  - Khan Academy (`khanacademy.org`)
  - Coursera (`coursera.org`)
  - edX (`edx.org`)
  - TED (`ted.com`)
  - Wikipedia (`wikipedia.org`)
  - Educational institution domains (`.edu`)
- **SHOULD** provide context-appropriate messaging for educational content

### EDU-05: Learning Management Systems
- **SHOULD** handle common LMS patterns and domains
- **SHOULD** recognize authentication-required educational resources
- **SHOULD** provide guidance for testing authenticated educational content
- **SHOULD** distinguish between blocked vs. authentication-required content

## Curriculum Support Features

### EDU-06: Subject-Specific Content
- **SHOULD** support bulk testing of subject-specific URL lists
- **SHOULD** handle educational content that may require specific browser features
- **SHOULD** recognize interactive educational content limitations
- **SHOULD** provide subject-area appropriate recommendations

### EDU-07: Accessibility Compliance
- **MUST** ensure the tool itself follows accessibility guidelines
- **SHOULD** flag educational content accessibility issues when detectable
- **SHOULD** provide guidance for accessible educational resource selection
- **SHOULD** support screen reader compatibility for the tool interface

## Content Policy Awareness

### EDU-08: School Content Filtering Context
- **MUST** understand that schools use content filtering for safety and compliance
- **MUST** distinguish between blocked vs. temporarily unavailable content
- **MUST** provide appropriate recommendations that respect school policies
- **MUST** avoid suggesting circumvention of legitimate content filters

### EDU-09: Educational Value Assessment
- **SHOULD** provide context about educational value of blocked resources
- **SHOULD** help prioritize unblocking requests based on educational importance
- **SHOULD** support documentation of educational necessity for IT requests
- **SHOULD** recognize difference between educational and entertainment content

## Integration with Educational Workflows

### EDU-10: Lesson Planning Support
- **MUST** support bulk testing of lesson plan URLs before class
- **MUST** provide quick verification of resource accessibility
- **MUST** generate reports suitable for backup resource identification
- **MUST** support efficient workflow for educators with time constraints

### EDU-11: Professional Development
- **SHOULD** support testing of professional development resources
- **SHOULD** handle educational conference and training material URLs
- **SHOULD** provide guidance for educators learning new digital tools
- **SHOULD** support institutional technology training programs

### EDU-12: Curriculum Committee Support
- **MUST** generate reports suitable for curriculum committee review
- **MUST** provide data for educational technology policy decisions
- **MUST** support systematic review of digital curriculum resources
- **MUST** enable evidence-based recommendations for resource adoption

## Safety and Compliance

### EDU-13: Student Safety Considerations
- **MUST** never bypass or circumvent school safety measures
- **MUST** respect COPPA and FERPA compliance requirements
- **MUST** avoid storing or transmitting student-related information
- **MUST** support school policies for digital safety

### EDU-13A: Personally Identifiable Information (PII) Display and Reporting
- **MUST** read and display human-determined PII flags from CSV data
- **MUST NOT** evaluate or assess PII requirements automatically
- **MUST** provide clear visual indicators for PII-flagged resources
- **MUST** organize PII-flagged resources prominently in results and reports
- **MUST** support administrative compliance review workflows
- **MUST** generate reports for contacting vendors about local privacy requirements
- **MUST** help schools identify resources requiring legal/policy review
- **MUST** distinguish between accessibility testing and privacy policy assessment

### EDU-13B: Administrative Privacy Support
- **MUST** help administrators organize resources flagged for privacy review
- **MUST** support systematic evaluation of human-identified PII resources
- **MUST** enable tracking of privacy considerations across curriculum resources
- **MUST** provide data for administrative compliance documentation
- **MUST** support institutional workflows for contacting vendors about local laws
- **MUST** generate vendor contact lists based on PII-flagged resources

### EDU-14: Age-Appropriate Content
- **SHOULD** recognize age-appropriate content considerations
- **SHOULD** support different testing contexts for different grade levels
- **SHOULD** provide appropriate recommendations for K-12 vs. higher education
- **SHOULD** understand developmental appropriateness in access recommendations

## Resource Prioritization and Importance

### EDU-15: Educational Priority Management
- **MUST** utilize importance/priority rankings when available in CSV data
- **MUST** prioritize testing and reporting by educational significance
- **MUST** highlight accessibility issues for high-importance resources
- **MUST** provide priority-weighted accessibility statistics
- **MUST** support resource prioritization for limited IT resources

### EDU-15A: Curriculum Critical Resources
- **MUST** identify and flag curriculum-critical resources (high importance values)
- **MUST** provide expedited review paths for essential educational tools
- **MUST** generate priority reports for immediate IT attention
- **MUST** support emergency access procedures for critical resources
- **MUST** distinguish between core curriculum and supplemental resources

### EDU-15B: Unit and Course Organization
- **MUST** organize results by educational unit/module when unit data available
- **MUST** provide course-level accessibility summaries
- **MUST** identify units with critical resource accessibility issues
- **MUST** support curriculum sequencing with resource availability data
- **MUST** enable unit-by-unit curriculum review and planning

### EDU-15C: Educational Impact Assessment
- **MUST** calculate importance-weighted accessibility metrics for curriculum evaluation
- **MUST** identify high-impact accessibility issues affecting critical educational content
- **MUST** provide data for educational continuity planning
- **MUST** support evidence-based curriculum technology decisions
- **MUST** enable assessment of digital equity across educational units

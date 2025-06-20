# School URL Accessibility Checker

A comprehensive tool designed to help educators and IT administrators test website accessibility from within school networks. This tool helps identify which educational resources and websites are reachable through your school's internet connection and firewall settings.

## 🎯 Purpose

This tool is specifically designed for schools to:
- Test if educational websites are accessible from the school network
- Identify sites that may be blocked by firewalls or content filters
- Provide clear, non-technical reports for educators and administrators
- Help IT teams understand which resources teachers need access to

## 🌐 Web-Based Tool (Recommended)

The main tool is a browser-based application (`index.html`) that provides an easy-to-use interface for testing URL accessibility.

### Features

- **Multiple Input Methods**: Upload CSV files, paste URLs directly, or load from Google Sheets
- **Smart Testing**: Uses multiple testing methods including favicon loading and direct fetch attempts
- **Manual Verification**: Built-in iframe testing for uncertain results
- **Detailed Logging**: Step-by-step logs showing exactly what was tested and why
- **User-Friendly Reports**: Clear, color-coded results with explanations
- **HTTP Security Detection**: Automatically flags HTTP-only sites that may cause browser warnings
- **No Extensions Required**: Works entirely within the browser without additional software

### How It Works

The tool uses several testing methods to determine accessibility:

1. **Favicon Test**: Attempts to load the site's favicon.ico file
2. **No-CORS Fetch**: Tests direct connectivity while respecting browser security
3. **HTTP Security Check**: Identifies URLs using insecure HTTP protocol
4. **Manual Testing**: Provides iframe-based verification for uncertain results

### ⚠️ HTTP Security Warnings

The tool automatically detects and flags websites using HTTP (instead of HTTPS) protocol. These sites may cause issues in modern school environments:

- **Browser Warnings**: Chrome, Firefox, and other browsers increasingly warn users about HTTP sites
- **Mixed Content Issues**: HTTPS school portals may block HTTP resources
- **Security Policies**: Many schools block HTTP sites as a security measure

**Recommendation**: When possible, use HTTPS versions of educational websites or request site administrators to enable HTTPS.

### Status Meanings

- **🟢 Fully Accessible**: Site loads completely and is fully functional
- **🟡 Partially Accessible**: Basic connectivity detected, but full access uncertain
- **🔵 Possibly Reachable**: Connection attempted but limited by browser security
- **🔴 Not Reachable**: Site appears blocked or unavailable from school network
- **⏱️ Timeout**: Site is very slow or partially blocked
- **⚠️ HTTP Warning**: Site is accessible but uses insecure HTTP protocol that may cause browser warnings

## 🚀 Getting Started

1. **Open the Tool**: Open the [GitHub Page](https://ricec-at-masonhs.github.io/can-i-access/) in any modern web browser
2. **Add URLs**: Either:
   - Upload a CSV file with a 'URL' column
   - Paste URLs directly (one per line)
   - Use the "Load Default URLs" button for testing
3. **Run Tests**: Click "Check URLs" to start testing
4. **Review Results**: View the detailed report with status and explanations
5. **Manual Testing**: Use "Manual Test" buttons for uncertain results

## 📝 Input Formats

### CSV Upload
Your CSV file must contain a column named "URL". Example:
```csv
URL,Description
https://www.khanacademy.org,Math education
https://scratch.mit.edu,Programming for kids
https://www.google.com/classroom,Google Classroom
```

### Direct Input
Paste URLs one per line:
```
https://www.example.com
https://www.educational-site.org
https://www.another-resource.edu
```

### Google Sheets Integration
Update the `DEFAULT_GOOGLE_SHEET_CSV_URL` variable in `script.js` to point to your published Google Sheet CSV.

## 🔧 Technical Details

### Browser Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- No additional extensions or plugins required

### Network Testing Methods
The tool is designed to work within browser security limitations:
- Uses `fetch()` with `no-cors` mode to test connectivity
- Employs favicon loading as a reliable connectivity indicator
- Provides manual iframe testing for definitive results
- Respects school firewall and security policies

### Files Structure
```
├── index.html          # Main web interface
├── script.js           # Core functionality and testing logic
├── style.css           # Styling and responsive design
├── test-urls.csv       # Sample URL list for testing
├── python-script/      # Alternative Python-based tool
│   └── url-check.py    # Command-line testing script
└── README.md           # This documentation
```

## 🐍 Python Alternative

For advanced users or situations where the web tool has limitations, a Python script is available:

```bash
cd python-script
python url-check.py                           # Test all predefined Google Sheets
python url-check.py --csv ../test-urls.csv    # Test custom CSV file  
python url-check.py --sheet cyber1            # Test specific Google Sheet
```

The Python script provides additional features:
- **Multiple Google Sheets**: Can process multiple predefined sheets (cyber1, cyber2, cyber3)
- **Detailed HTML Reports**: Generates professional styled reports with summary cards
- **HTTP Detection**: Flags insecure HTTP-only URLs with warnings
- **Command Line Options**: Supports custom CSV files and specific sheets

The Python script avoids browser security restrictions but requires:
- Python 3.x installed
- `requests` library (`pip install requests`)
- Network access from the machine running the script
- Command-line interface familiarity

## 🎨 Customization

### Adding Default URLs
Edit the `DEFAULT_GOOGLE_SHEET_CSV_URL` in `script.js` to point to your own Google Sheet:

1. Create a Google Sheet with a 'URL' column
2. Go to File > Share > Publish to web
3. Choose "Comma-separated values (.csv)" format
4. Copy the generated URL
5. Replace the placeholder URL in `script.js`

### Styling
Modify `style.css` to match your school's branding or accessibility requirements.

## 🤝 Use Cases

### For Educators
- Test if lesson plan websites are accessible before class
- Verify educational resources work from school computers
- Identify alternative resources when primary sites are blocked
- Spot potential browser security warnings for HTTP sites

### For IT Administrators
- Audit which educational sites are accessible
- Generate reports for firewall policy updates
- Test connectivity after network changes
- Provide evidence for unblocking educational resources
- Identify HTTP sites that may need security policy updates

### For Curriculum Coordinators
- Ensure digital resources in curriculum guides are accessible
- Test new educational platforms before district-wide adoption
- Verify accessibility across different school buildings
- Identify security concerns with HTTP-only educational sites

## 🔒 Privacy & Security

- All testing is performed locally in your browser
- No data is sent to external services (except for testing the URLs themselves)
- Results are not stored or transmitted anywhere
- Tool respects school network security policies

## 📚 Troubleshooting

### "Partially Accessible" Results
- Use the "Manual Test" button to verify actual accessibility
- Check if the site loads properly in the iframe
- Some sites may block iframe embedding but work in regular tabs

### "Not Reachable" Results
- Verify the URL is correct and currently online
- Check if the site requires specific protocols (HTTP vs HTTPS)
- Contact IT team if educational resource appears incorrectly blocked

### HTTP Warning Results
- Site works but uses insecure HTTP protocol
- Modern browsers may show security warnings to users
- Consider finding HTTPS alternatives or requesting site upgrades
- Test in actual classroom environment to verify student experience

### Tool Not Working
- Ensure JavaScript is enabled in your browser
- Check browser console for error messages
- Try refreshing the page and testing again

## 📄 License

This project is open source. See `LICENSE` file for details.

---

**Note**: This tool is designed for educational and administrative use within school networks. Always follow your organization's IT policies and procedures when testing network accessibility.
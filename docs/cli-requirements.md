# CLI Tool Requirements

## Zero External Dependencies

This tool is designed to have **ZERO external dependencies** to ensure maximum compatibility with educational environments.

## System Requirements

### Python Version
- **Minimum**: Python 3.6+
- **Recommended**: Python 3.8+ for best performance
- **Tested**: Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12

### Operating Systems
- ✅ **Windows** 10+ (PowerShell, Command Prompt)
- ✅ **macOS** 10.14+ (Terminal, Zsh, Bash)
- ✅ **Linux** distributions with Python 3.6+
- ✅ **Chrome OS** (Linux development environment)

## Standard Library Dependencies Only

The tool uses only Python standard library modules:

### Core Functionality
- **`urllib.request`** - HTTP/HTTPS requests
- **`urllib.parse`** - URL parsing and validation
- **`urllib.error`** - HTTP error handling
- **`socket`** - Network connectivity testing
- **`ssl`** - HTTPS/TLS support

### Data Processing
- **`csv`** - CSV file reading and writing
- **`json`** - JSON output formatting
- **`re`** - Regular expression pattern matching
- **`io`** - String and file I/O operations

### User Interface
- **`argparse`** - Command-line argument parsing
- **`textwrap`** - Text formatting and wrapping
- **`sys`** - System interaction and exit codes
- **`os`** - File system operations

### Utilities
- **`time`** - Request timing and timeouts
- **`datetime`** - Timestamp generation
- **`pathlib`** - Cross-platform file path handling
- **`concurrent.futures`** - Parallel request processing

## Installation Requirements

### What You DON'T Need
- ❌ **No pip install** required
- ❌ **No virtual environments** needed
- ❌ **No package managers** (conda, poetry, etc.)
- ❌ **No external libraries** (requests, pandas, etc.)
- ❌ **No administrative privileges** for setup
- ❌ **No internet connection** for installation

### What You DO Need
- ✅ **Python 3.6+** installed on the system
- ✅ **Network access** to test URLs (at runtime only)
- ✅ **File system access** to read CSV files and write reports

## Educational Environment Benefits

### School Computer Compatibility
- **Works immediately** on any system with Python
- **No IT approval** needed for external packages
- **Runs from USB drives** or network shares
- **No system modifications** required
- **Portable execution** from any directory

### Restricted Network Compatibility
- **Respects proxy settings** automatically
- **Uses standard ports** (80, 443) only
- **No bypass attempts** of network filters
- **Firewall friendly** HTTP/HTTPS only
- **Air-gap compatible** for installation

### Security Benefits
- **No external code** downloaded at runtime
- **No telemetry** or data collection
- **Local processing only** - all data stays on device
- **Transparent operation** - open source with no hidden dependencies
- **Minimal attack surface** - standard library only

## Performance Characteristics

### Resource Usage
- **Memory**: < 50MB typical usage
- **Disk Space**: < 5MB for all files
- **CPU**: Minimal impact during URL testing
- **Network**: Only when actively testing URLs

### Scalability
- **Parallel processing**: 1-10 concurrent requests (configurable)
- **Large datasets**: Tested with 1000+ URLs
- **CSV files**: Handles files up to 100MB+
- **Report generation**: Efficient HTML/JSON output

## Quality Assurance

### Testing Coverage
- ✅ **Cross-platform**: Windows, macOS, Linux
- ✅ **Python versions**: 3.6 through 3.12
- ✅ **Network conditions**: Fast, slow, filtered networks
- ✅ **CSV formats**: Various encodings and structures
- ✅ **Edge cases**: Malformed URLs, timeouts, errors

### Educational Environment Testing
- ✅ **School networks** with content filters
- ✅ **Slow connections** with high latency
- ✅ **Restricted computers** without admin access
- ✅ **USB deployment** on multiple machines
- ✅ **Various Python installations** (system, anaconda, etc.)

## Deployment Scenarios

### Scenario 1: Individual Teacher
```bash
# Download files to desktop
# Run immediately without setup
python -m can_i_access --help
```

### Scenario 2: IT Department
```bash
# Deploy to network share
# Students access via mapped drive
# No installation on individual machines
```

### Scenario 3: Classroom Lab
```bash
# Install on lab computers once
# Students run from Start menu shortcut
# Results save to student directories
```

### Scenario 4: Home/Remote Learning
```bash
# Email zip file to students
# Extract and run on personal computers
# Works with any Python installation
```

This zero-dependency architecture ensures the CLI tool can be deployed in **any** educational environment without requiring complex setup procedures, administrative approval for external packages, or internet connectivity during installation.

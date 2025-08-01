# Can I Access? CLI Tool

A zero-dependency command-line tool for testing website accessibility in educational networks. Perfect for teachers, IT administrators, and curriculum planners who need to verify which educational websites are accessible on school networks.

## ⚡ Quick Start

### 1. Download and Run
```bash
# Option 1: Clone from GitHub (if you have git)
git clone https://github.com/RiceC-at-MasonHS/can-i-access.git
cd can-i-access/python-script

# Option 2: Download ZIP from GitHub
# Go to: https://github.com/RiceC-at-MasonHS/can-i-access
# Click "Code" → "Download ZIP" → Extract → Navigate to python-script/

# Run immediately (no installation required!)
python -m can_i_access --help
```

### 2. Test Some URLs
```bash
# Test default cybersecurity curriculum
python -m can_i_access

# Test a single website
python -m can_i_access --url https://example.com

# Test from your CSV file
python -m can_i_access --csv your-urls.csv
```

### 3. Get Professional Reports
```bash
# Generate HTML report
python -m can_i_access --csv your-urls.csv --output results.json
python -m can_i_access report results.json --format html -o report.html
```

## 🎯 Why Use This Tool?

- **Zero Dependencies** - Works immediately with Python 3.6+, no pip install needed
- **School-Network Friendly** - Designed for restricted environments
- **Educational Focus** - Built-in curricula and privacy compliance features
- **Professional Reports** - Generate reports for IT departments and administration
- **Easy for Beginners** - Clear documentation and helpful error messages
- **Complements Web Version** - Use web tool for quick tests, CLI for batch processing

💡 **Quick Test?** Try the web version: https://ricec-at-masonhs.github.io/can-i-access/

## 📋 Basic Commands

### Testing URLs
```bash
# Test built-in curriculum lists
python -m can_i_access --cyber1           # Cybersecurity curriculum
python -m can_i_access --all-cyber        # All cyber curricula

# Test your own URLs
python -m can_i_access --url https://site.com
python -m can_i_access --csv my-urls.csv

# Test with filtering
python -m can_i_access --csv urls.csv --filter blocked
python -m can_i_access --csv urls.csv --filter pii-required
```

### Getting Information
```bash
python -m can_i_access --help             # Quick help
python -m can_i_access --man              # Full manual
python -m can_i_access list --sources     # Available curricula
python -m can_i_access list --formats     # Output formats
```

### Advanced Features
```bash
# Parallel testing for speed
python -m can_i_access --csv big-list.csv --parallel 5

# Verbose output for debugging
python -m can_i_access --url site.com -vv

# Different output formats
python -m can_i_access --csv urls.csv --format json
python -m can_i_access --csv urls.csv --format csv
```

## 📊 CSV File Format

Your CSV files should have these columns (only `url` is required):

```csv
url,site,unit,importance,pii
https://example.com,Example Site,Unit 1,high,false
https://github.com,GitHub,Unit 2,medium,false
https://youtube.com/watch?v=123,Demo Video,Unit 1,high,true
```

### Column Descriptions:
- **url** (required) - The website URL to test
- **site** (optional) - Human-readable site name
- **unit** (optional) - Curriculum unit or category  
- **importance** (optional) - Priority level: high, medium, low
- **pii** (optional) - Whether site requires personal info: true, false

## 🔧 Setup for New Python Users

### Option 1: Simple Setup (Recommended)
```bash
# Download the files, then:
python setup.py
```
This creates shortcuts and shows you exactly how to run the tool.

### Option 2: Interactive Tutorial
```bash
python quick-start-demo.py
```
Walks you through all the features step-by-step.

### Option 3: Manual
Just run `python -m can_i_access --help` and start exploring!

## 📈 Common Workflows

### For Teachers
```bash
# Check if curriculum websites work
python -m can_i_access --cyber1

# Test your lesson plan URLs
python -m can_i_access --csv lesson-sites.csv --filter blocked
```

### For IT Administrators  
```bash
# Generate reports for network review
python -m can_i_access --csv all-educational-sites.csv --output review.json
python -m can_i_access report review.json --format html -o network-report.html

# Check high-priority sites only
python -m can_i_access --csv sites.csv --filter importance:high
```

### For Curriculum Planners
```bash
# Review sites requiring personal information
python -m can_i_access --csv curriculum.csv --filter pii-required

# Export accessible sites for lesson planning
python -m can_i_access --csv all-sites.csv --filter accessible --format csv -o approved-sites.csv
```

## 🛟 Troubleshooting

### "Command not found" or "Module not found"
- Make sure you're in the `python-script` directory
- Use `python -m can_i_access` instead of just `can_i_access`
- Check that Python 3.6+ is installed: `python --version`

### "Permission denied" errors
- You might be on a restricted school computer
- Try adding `--timeout 10` for slower networks
- Contact IT if you need help with network policies

### CSV parsing errors  
- Make sure your CSV has a `url` column
- Check for special characters in URLs
- Use the sample CSV as a template

### Need more help?
```bash
python -m can_i_access --man              # Full documentation
python quick-start-demo.py                # Interactive tutorial
```

## 🎓 Educational Features

- **Built-in Curricula** - Cybersecurity, computer science, and digital literacy
- **Privacy Compliance** - PII flags for COPPA/FERPA considerations  
- **Network Respect** - Tests accessibility without attempting to bypass filters
- **Professional Output** - Generate reports that IT departments understand
- **Bulk Testing** - Efficiently check hundreds of educational websites

## 🔒 Privacy & Security

- **No Data Collection** - Everything runs locally on your computer
- **No External Dependencies** - Uses only Python standard library
- **Firewall Friendly** - Respects school network policies
- **Open Source** - Full transparency in testing methods

## 📝 License

MIT License - feel free to use this in your educational environment!

## 🤝 Contributing

Found a bug or have a feature request? 
- Open an issue on GitHub
- Submit a pull request
- Contact the maintainers

## 🌐 Web Version

Need a quick test without installing anything? Try the web version:
**https://ricec-at-masonhs.github.io/can-i-access/**

Perfect for:
- ✅ **Quick single URL tests** - No setup required
- ✅ **Small CSV files** - Drag and drop testing  
- ✅ **Demonstrating to colleagues** - Works in any browser
- ✅ **Mobile devices** - Responsive design

The CLI tool is ideal for:
- ✅ **Large datasets** - Process hundreds of URLs efficiently
- ✅ **Professional reports** - Generate HTML/CSV reports for IT
- ✅ **Batch processing** - Automated testing workflows
- ✅ **Advanced filtering** - PII compliance and importance ranking

---

**Questions?** Check the full manual with `python -m can_i_access --man` or run the interactive tutorial with `python quick-start-demo.py`

# Can I Access? 🌐

**The essential toolkit for educational website accessibility testing in school networks**

[![GitHub Pages](https://img.shields.io/badge/Try%20It%20Now-GitHub%20Pages-blue)](https://ricec-at-masonhs.github.io/can-i-access/) [![Python CLI](https://img.shields.io/badge/Download-CLI%20Tool-green)](https://github.com/RiceC-at-MasonHS/can-i-access/tree/main/python-script) [![Documentation](https://img.shields.io/badge/📚-Full%20Docs-orange)](https://github.com/RiceC-at-MasonHS/can-i-access/tree/main/docs)

---

## 🎯 **What This Project Offers**

**Can I Access?** provides two complementary tools to help educators, IT administrators, and curriculum planners test which educational websites work on school networks:

### 🌐 **[Web Tool](https://ricec-at-masonhs.github.io/can-i-access/)** - *Quick & Easy*
Perfect for immediate testing and demonstration
- ✅ **Zero installation** - Works in any browser  
- ✅ **Drag & drop CSV testing** - Instant results
- ✅ **Mobile-friendly** - Test from anywhere
- ✅ **Perfect for sharing** - Send colleagues a link

### 💻 **[CLI Tool](python-script/)** - *Powerful & Professional*
Ideal for batch processing and professional reporting
- ✅ **Zero dependencies** - Uses only Python standard library
- ✅ **Batch processing** - Test hundreds of URLs efficiently  
- ✅ **Professional reports** - Generate HTML/CSV reports for IT
- ✅ **Advanced filtering** - PII compliance and importance ranking

---

## 🚀 **Get Started in 30 Seconds**

### **Quick Test** (No installation)
1. 🌐 **[Open the web tool](https://ricec-at-masonhs.github.io/can-i-access/)**
2. 📋 **Paste some URLs** or drag in a CSV file
3. ▶️ **Click "Check URLs"** and see instant results!

### **Professional Analysis** (For IT/power users)  
1. 📥 **[Download the CLI tool](https://github.com/RiceC-at-MasonHS/can-i-access/archive/refs/heads/main.zip)**
2. 📂 **Extract and navigate** to `can-i-access/python-script/`
3. ⚡ **Run:** `python -m can_i_access --help`

---

## 🎓 **Perfect for Education**

### **👩‍🏫 For Teachers**
- **Before class:** Test if lesson websites work on school computers
- **During planning:** Check educational resources for accessibility  
- **Quick verification:** Use web tool for immediate answers

### **👨‍💻 For IT Administrators**  
- **Policy auditing:** Generate reports on blocked educational sites
- **Bulk testing:** Process curriculum lists with [CLI tool](python-script/) 
- **Compliance reporting:** Track sites requiring student PII

### **📚 For Curriculum Coordinators**
- **Resource validation:** Ensure digital curriculum works district-wide
- **Platform evaluation:** Test new educational tools before adoption
- **Standards compliance:** Generate professional reports for administration

---

## �️ **Core Features**

### **Smart Testing Technology**
- **Multi-method verification** - Favicon, HTTPS upgrade, direct connectivity
- **YouTube detection** - Special handling for educational videos  
- **Security compliance** - Flags HTTP sites that cause browser warnings
- **Firewall respect** - Tests accessibility without bypass attempts

### **Educational Focus** 
- **Built-in curricula** - Cybersecurity, computer science, digital literacy
- **Privacy compliance** - PII handling for COPPA/FERPA
- **Professional reporting** - IT-friendly documentation and recommendations
- **Bulk processing** - Handle entire curriculum lists efficiently

### **Zero Hassle Deployment**
- **Web version:** Works immediately in any browser
- **CLI version:** [Zero external dependencies](docs/python-version/requirements.md) - just Python 3.6+
- **School-friendly:** No administrative privileges needed
- **Cross-platform:** Windows, macOS, Linux compatible

---

## 📊 **Choose Your Tool**

| Feature | 🌐 **Web Tool** | 💻 **CLI Tool** |
|---------|----------------|-----------------|
| **Setup Time** | 0 seconds | 30 seconds |
| **Best For** | Quick tests, demos | Batch processing, reports |
| **CSV Support** | ✅ Drag & drop | ✅ Advanced processing |
| **Mobile Friendly** | ✅ Yes | ❌ Desktop only |
| **Bulk Testing** | Small lists | Hundreds of URLs |
| **Professional Reports** | Basic | ✅ HTML/CSV/JSON |
| **Privacy Filtering** | Manual | ✅ Automated |
| **Curriculum Integration** | Manual upload | ✅ Built-in datasets |

---

## 🗂️ **Project Structure**

```
can-i-access/
├── 🌐 index.html              # Web tool (GitHub Pages)
├── 📜 script.js               # Web tool functionality  
├── 🎨 style.css               # Web tool styling
├── 💻 python-script/          # CLI tool directory
│   ├── 📖 README.md           # CLI user guide
│   ├── 🚀 setup.py            # Quick setup helper
│   ├── 🎮 quick-start-demo.py # Interactive tutorial
│   ├── 📊 sample-urls.csv     # Example CSV for testing
│   └── 📦 can_i_access/       # Core CLI package
├── 📚 docs/                   # Technical documentation
│   ├── 📋 README.md           # Documentation organization guide
│   ├── 🤝 shared/             # Common requirements (both tools)
│   ├── 🌐 web-version/        # Browser tool requirements
│   └── � python-version/      # CLI tool requirements & bug fixes
├── 📊 cyber1-allow-list.csv   # Sample educational URLs
└── 🧪 test-*.csv              # Various test datasets
```

---

## 📖 **Documentation Deep Dive**

### **📋 Requirements & Architecture**
- **[Python CLI Requirements](docs/python-version/requirements.md)** - Zero-dependency architecture and features
- **[Web Tool Requirements](docs/web-version/requirements.md)** - Browser compatibility and UI specifications
- **[Project Overview](docs/shared/project-overview.md)** - Purpose, audiences, and value proposition

### **🎯 Educational Integration**  
- **[Core Functionality](docs/shared/core-functionality.md)** - URL testing, CSV processing, educational content
- **[Quality Assurance](docs/python-version/quality-assurance.md)** - Testing and validation procedures
- **[Bug Fixes & Development](docs/python-version/bug-fixes.md)** - Recent improvements and current issues

### **📊 Professional Features**
- **[CLI Quality Assurance](docs/python-version/quality-assurance.md)** - Professional testing requirements
- **[Web Quality Assurance](docs/web-version/quality-assurance.md)** - Browser testing and validation
- **[Documentation Organization](docs/README.md)** - Guide to reorganized requirements structure

---

## 🎨 **Real-World Usage Examples**

### **Scenario 1: Teacher Prep** 
```bash
# Quick check before class
🌐 Open web tool → Paste lesson URLs → Instant results
```

### **Scenario 2: IT Audit**
```bash
# Professional district-wide analysis  
💻 Download CLI → Load curriculum CSV → Generate IT report
python -m can_i_access --csv district-sites.csv --output audit.json
python -m can_i_access report audit.json --format html -o it-report.html
```

### **Scenario 3: Curriculum Review**
```bash
# Filter by privacy requirements
💻 python -m can_i_access --csv curriculum.csv --filter pii-required
```

---

## 🔒 **Privacy & Security Promise**

- ✅ **No data collection** - Everything runs locally  
- ✅ **No external dependencies** - CLI uses only Python standard library
- ✅ **Firewall friendly** - Respects school network policies  
- ✅ **Open source** - Full transparency in testing methods
- ✅ **Educational focus** - Built specifically for school environments

---

## 🤝 **Contributing & Support**

### **Get Involved**
- 🐛 **[Report Issues](https://github.com/RiceC-at-MasonHS/can-i-access/issues)** - Help improve the tools
- 💡 **[Request Features](https://github.com/RiceC-at-MasonHS/can-i-access/discussions)** - Suggest educational integrations
- 📖 **[Improve Documentation](docs/)** - Help other educators

### **Need Help?**
- 🌐 **Web tool issues:** Check browser console, try refresh
- 💻 **CLI tool help:** Run `python -m can_i_access --man` for full manual
- 📚 **Educational integration:** See [documentation](docs/) for curriculum guides

---

## 📄 **License**

MIT License - Free for educational and commercial use. See [LICENSE](LICENSE) for details.

---

<div align="center">

**🎓 Built for Education • 🔒 Privacy-First • 🌍 Open Source**

[**🌐 Try Web Tool**](https://ricec-at-masonhs.github.io/can-i-access/) • [**💻 Download CLI**](python-script/) • [**📚 Read Docs**](docs/)

*Making educational technology accessible in every classroom*

</div>
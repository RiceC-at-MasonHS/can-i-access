# CLI Tool Developer Reference

## Quick File Guide

### User-Facing Files (python-script/)
- **`README.md`** - Main user documentation, getting started guide
- **`can-i-access`** - Direct executable script (Unix/Linux)  
- **`setup.py`** - One-time setup helper for new users
- **`quick-start-demo.py`** - Interactive tutorial
- **`sample-urls.csv`** - Example CSV file for testing

### Core Implementation (python-script/can_i_access/)
- **`__init__.py`** - Main module with core functionality and CLI framework
- **`__main__.py`** - Module entry point for `python -m can_i_access`
- **`commands/`** - Command implementations (test, list, report)

### Documentation & Metadata (docs/)
- **`cli-redesign-summary.md`** - Complete redesign documentation
- **`cli-requirements.txt`** - Zero-dependency requirements
- **`cli-technical-requirements.md`** - Technical architecture details
- **`01-09-*.md`** - Original project requirements documentation

## Key Architecture Principles

1. **Zero Dependencies** - Only Python standard library
2. **Educational Focus** - Designed for school network environments  
3. **Linux-Style CLI** - Professional command-line interface
4. **Modular Design** - Separate commands in dedicated modules
5. **User-Friendly** - Clear documentation and error messages

## Development Commands

```bash
# Test the CLI
python -m can_i_access --help
python -m can_i_access --url example.com

# Run interactive demo
python quick-start-demo.py

# Test CSV processing
python -m can_i_access --csv sample-urls.csv

# Generate reports
python -m can_i_access --csv sample-urls.csv --output test.json
python -m can_i_access report test.json --format html -o test.html
```

## File Organization Logic

### User Experience Priority
- **Immediate access**: Core files in `python-script/` for direct use
- **Clear entry point**: README.md is the first thing users see
- **No clutter**: Technical metadata moved to `docs/`
- **Sample data**: Included for immediate testing

### Technical Separation  
- **Requirements-as-Code**: Technical docs in version-controlled `docs/`
- **Generated files ignored**: Test outputs excluded from git
- **Clean deployment**: Users get only essential files
- **Maintainer docs**: Separate from user-facing documentation

This organization ensures users see a clean, focused tool while developers have access to comprehensive technical documentation.

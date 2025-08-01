"""
List command implementation - show available data sources and formats
"""

import sys
from .. import Colors, PREDEFINED_SHEETS

def run_list_command(args):
    """Execute the list command"""
    if args.sources:
        list_data_sources()
    elif args.formats:
        list_output_formats()
    else:
        # Default: show both
        list_data_sources()
        print()
        list_output_formats()

def list_data_sources():
    """List available predefined data sources"""
    print(f"{Colors.BOLD}{Colors.BLUE}Available Data Sources{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Predefined Cybersecurity Curricula:{Colors.END}")
    for name, url in PREDEFINED_SHEETS.items():
        print(f"  {Colors.GREEN}--{name}{Colors.END}")
        print(f"    {Colors.CYAN}{url}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Custom Sources:{Colors.END}")
    print(f"  {Colors.GREEN}--csv FILE{Colors.END}")
    print(f"    Load URLs from local CSV file")
    print(f"  {Colors.GREEN}--sheet URL{Colors.END}")
    print(f"    Load URLs from published Google Sheets CSV")
    print(f"  {Colors.GREEN}--url URL{Colors.END}")
    print(f"    Test a single URL")
    
    print(f"\n{Colors.BOLD}CSV Format Requirements:{Colors.END}")
    print(f"  Required column: {Colors.YELLOW}'URL'{Colors.END}")
    print(f"  Optional columns:")
    print(f"    {Colors.CYAN}'site'{Colors.END} - Resource name")
    print(f"    {Colors.CYAN}'unit'{Colors.END} - Educational unit number")
    print(f"    {Colors.CYAN}'reporting z-index (higher, more important)'{Colors.END} - Priority ranking")
    print(f"    {Colors.CYAN}'Student PII Needed'{Colors.END} - Privacy flag (TRUE/FALSE)")

def list_output_formats():
    """List available output formats"""
    print(f"{Colors.BOLD}{Colors.BLUE}Output Formats{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}")
    
    formats = [
        ('text', 'Human-readable colored output (default)', 'Terminal display, progress updates'),
        ('json', 'Machine-readable JSON format', 'Automation, further processing'),
        ('csv', 'Comma-separated values', 'Spreadsheet import, data analysis'),
        ('html', 'HTML report (via report command)', 'Web viewing, professional reports')
    ]
    
    for fmt, description, use_case in formats:
        print(f"\n{Colors.GREEN}{fmt}{Colors.END}")
        print(f"  {description}")
        print(f"  {Colors.CYAN}Use case: {use_case}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Filter Options:{Colors.END}")
    filters = [
        ('all', 'Show all results (default)'),
        ('blocked', 'Show only blocked/unreachable URLs'),
        ('accessible', 'Show only accessible URLs'),
        ('warnings', 'Show only URLs with warnings')
    ]
    
    for filt, description in filters:
        print(f"  {Colors.YELLOW}--filter {filt}{Colors.END}: {description}")
    
    print(f"\n{Colors.BOLD}Examples:{Colors.END}")
    print(f"  {Colors.CYAN}can-i-access --cyber1 --format json --output results.json{Colors.END}")
    print(f"  {Colors.CYAN}can-i-access --csv urls.csv --filter blocked{Colors.END}")
    print(f"  {Colors.CYAN}can-i-access report results.json --format html -o report.html{Colors.END}")

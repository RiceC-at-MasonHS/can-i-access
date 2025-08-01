#!/usr/bin/env python3
"""
Can I Access? - School Network URL Accessibility Checker (CLI Edition)

A command-line tool for testing educational website accessibility from within
school networks. Uses only Python standard library - no external dependencies.

This tool helps educators and IT administrators verify which educational
resources are accessible from their school's network, identifying potential
firewall blocks or connectivity issues.

Author: GitHub.com/RiceC-at-MasonHS
License: MIT
"""

import sys
import os
import argparse
import textwrap
from urllib.parse import urlparse
from urllib.request import urlopen, Request, HTTPError, URLError
from urllib.error import URLError
import csv
import json
import time
import re
from datetime import datetime
import socket
import ssl

# Version info
__version__ = "2.0.0"
__author__ = "RiceC-at-MasonHS"

# Configuration constants
DEFAULT_TIMEOUT = 10
USER_AGENT = "CanIAccess/2.0 (Educational Network Testing Tool)"
MAX_REDIRECTS = 5

# Predefined Google Sheets for educational content
PREDEFINED_SHEETS = {
    'cyber1': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT9Oz-V5oBf5R0CTfGJl0BTnHf54zn0YEHKd6VvNYNWajK__z09mlyHmvH_6yjx4gpo319Ld4JgYxjY/pub?gid=0&single=true&output=csv',
    'cyber2': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT9Oz-V5oBf5R0CTfGJl0BTnHf54zn0YEHKd6VvNYNWajK__z09mlyHmvH_6yjx4gpo319Ld4JgYxjY/pub?gid=1898941805&single=true&output=csv',
    'cyber3': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT9Oz-V5oBf5R0CTfGJl0BTnHf54zn0YEHKd6VvNYNWajK__z09mlyHmvH_6yjx4gpo319Ld4JgYxjY/pub?gid=1535267557&single=true&output=csv'
}

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @classmethod
    def disable(cls):
        """Disable color output"""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = ''
        cls.MAGENTA = cls.CYAN = cls.WHITE = cls.BOLD = ''
        cls.UNDERLINE = cls.END = ''

def eprint(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)

def format_url_for_display(url, max_length=60):
    """Format URL for display, truncating if necessary"""
    if len(url) <= max_length:
        return url
    return url[:max_length-3] + "..."

def is_youtube_url(url):
    """Check if URL is a YouTube video"""
    youtube_patterns = [
        r'youtube\.com/watch\?v=',
        r'youtu\.be/',
        r'youtube\.com/embed/',
        r'youtube\.com/v/'
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in youtube_patterns)

def extract_youtube_video_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)',
        r'youtube\.com/v/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def check_youtube_video(video_id, timeout=10):
    """Check if YouTube video is available using oEmbed API"""
    if not video_id:
        return {"available": False, "reason": "Invalid video ID"}
    
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    
    try:
        req = Request(oembed_url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                return {"available": True, "reason": "Video accessible"}
            else:
                return {"available": False, "reason": f"HTTP {response.status}"}
    except HTTPError as e:
        if e.code == 404:
            return {"available": False, "reason": "Video not found or private"}
        else:
            return {"available": False, "reason": f"HTTP error {e.code}"}
    except (URLError, socket.timeout, ssl.SSLError) as e:
        return {"available": False, "reason": f"Network error: {str(e)}"}

def attempt_https_upgrade(url):
    """Try to upgrade HTTP URL to HTTPS"""
    if not url.lower().startswith('http://'):
        return url, False
    
    https_url = url.replace('http://', 'https://', 1)
    
    try:
        # Quick test with a HEAD request
        req = Request(https_url, headers={'User-Agent': USER_AGENT})
        req.get_method = lambda: 'HEAD'
        
        with urlopen(req, timeout=5) as response:
            if response.status < 400:
                return https_url, True
    except:
        pass
    
    return url, False

def check_url_accessibility(url, timeout=DEFAULT_TIMEOUT, verbose=False):
    """
    Check if a URL is accessible from the current network.
    
    Args:
        url (str): URL to check
        timeout (int): Request timeout in seconds
        verbose (bool): Enable verbose output
        
    Returns:
        dict: Result dictionary with status, message, and metadata
    """
    original_url = url
    https_upgraded = False
    
    # Initialize result structure
    result = {
        'url': original_url,
        'final_url': url,
        'status': 'Error',
        'http_status': 'N/A',
        'message': 'Unknown error',
        'method': 'Unknown',
        'is_http_only': False,
        'https_upgraded': False,
        'is_youtube': False,
        'video_available': None,
        'response_time': 0,
        'site_name': '',
        'unit': '',
        'importance': 0,
        'pii_required': False
    }
    
    start_time = time.time()
    
    try:
        # Parse URL to validate
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            result['message'] = "Invalid URL format"
            return result
        
        # Check for HTTPS upgrade opportunity
        if url.lower().startswith('http://'):
            if verbose:
                print(f"  → Attempting HTTPS upgrade for {url}")
            upgraded_url, upgraded = attempt_https_upgrade(url)
            if upgraded:
                url = upgraded_url
                https_upgraded = True
                result['https_upgraded'] = True
                result['final_url'] = url
                if verbose:
                    print(f"  ✓ HTTPS upgrade successful: {url}")
            else:
                result['is_http_only'] = True
                if verbose:
                    print(f"  ⚠ HTTPS upgrade failed, using HTTP")
        
        # Special handling for YouTube URLs
        if is_youtube_url(url):
            result['is_youtube'] = True
            video_id = extract_youtube_video_id(url)
            
            if video_id:
                if verbose:
                    print(f"  → Checking YouTube video availability: {video_id}")
                
                youtube_check = check_youtube_video(video_id, timeout)
                result['video_available'] = youtube_check['available']
                
                if not youtube_check['available']:
                    result['status'] = 'Video Removed'
                    result['http_status'] = '404'
                    result['message'] = f"YouTube video unavailable: {youtube_check['reason']}"
                    result['method'] = 'YouTube oEmbed'
                    result['response_time'] = time.time() - start_time
                    return result
        
        # Attempt connection
        if verbose:
            print(f"  → Testing connectivity to {format_url_for_display(url)}")
        
        req = Request(url, headers={
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        with urlopen(req, timeout=timeout) as response:
            result['http_status'] = response.status
            result['response_time'] = time.time() - start_time
            
            if response.status < 400:
                # Success - determine specific status
                if result['is_http_only']:
                    result['status'] = 'Reachable (HTTP Warning)'
                    result['message'] = "⚠️ Site accessible but uses insecure HTTP. Modern browsers may show warnings."
                elif https_upgraded:
                    if result['is_youtube'] and result['video_available']:
                        result['status'] = 'Fully Accessible (Video Available, HTTPS Upgraded)'
                        result['message'] = "✓ YouTube video accessible with HTTPS upgrade"
                    elif result['is_youtube']:
                        result['status'] = 'Fully Accessible (HTTPS Upgraded)'
                        result['message'] = "✓ Site accessible with HTTPS upgrade"
                    else:
                        result['status'] = 'Fully Accessible (HTTPS Upgraded)'
                        result['message'] = "✓ Site accessible with HTTPS upgrade"
                else:
                    if result['is_youtube'] and result['video_available']:
                        result['status'] = 'Fully Accessible (Video Available)'
                        result['message'] = "✓ YouTube video fully accessible"
                    else:
                        result['status'] = 'Fully Accessible'
                        result['message'] = "✓ Site fully accessible"
                
                result['method'] = 'HTTP Request'
            else:
                result['status'] = 'Not Reachable'
                result['message'] = f"HTTP error {response.status}"
                result['method'] = 'HTTP Request'
    
    except HTTPError as e:
        result['http_status'] = e.code
        result['response_time'] = time.time() - start_time
        result['status'] = 'Not Reachable'
        result['message'] = f"HTTP {e.code}: {e.reason}"
        result['method'] = 'HTTP Request'
        
    except (URLError, socket.timeout, socket.gaierror, ssl.SSLError) as e:
        result['response_time'] = time.time() - start_time
        result['status'] = 'Not Reachable'
        result['method'] = 'HTTP Request'
        
        if isinstance(e, socket.timeout):
            result['message'] = f"Timeout after {timeout}s - site may be blocked or very slow"
        elif isinstance(e, socket.gaierror):
            result['message'] = f"DNS resolution failed - site may not exist or DNS is blocked"
        elif isinstance(e, ssl.SSLError):
            result['message'] = f"SSL/TLS error - certificate or security issue"
        else:
            result['message'] = f"Network error: {str(e)}"
    
    except Exception as e:
        result['response_time'] = time.time() - start_time
        result['status'] = 'Error'
        result['message'] = f"Unexpected error: {str(e)}"
        result['method'] = 'HTTP Request'
    
    return result

def main():
    """Main entry point"""
    # Parse command line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Handle special commands
    if args.version:
        print(f"Can I Access? v{__version__}")
        print(f"Author: {__author__}")
        print("GitHub: https://github.com/RiceC-at-MasonHS/can-i-access")
        sys.exit(0)
    
    if args.man:
        show_manual()
        sys.exit(0)
    
    # Configure output
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()
    
    # Run the appropriate command
    if args.command == 'test':
        from .commands.test import run_test_command
        run_test_command(args)
    elif args.command == 'list':
        from .commands.list import run_list_command
        run_list_command(args)
    elif args.command == 'report':
        from .commands.report import run_report_command
        run_report_command(args)
    else:
        # Default behavior - run test
        from .commands.test import run_test_command
        run_test_command(args)

def create_argument_parser():
    """Create the argument parser with all options"""
    parser = argparse.ArgumentParser(
        prog='can-i-access',
        description='Test educational website accessibility from school networks',
        epilog=textwrap.dedent("""
        examples:
          %(prog)s                          # Test default educational URLs
          %(prog)s --csv urls.csv           # Test URLs from CSV file
          %(prog)s --url example.com        # Test single URL
          %(prog)s --cyber1                 # Test only Cyber1 curriculum
          %(prog)s --output report.json     # Save results to JSON
          %(prog)s --man                    # Show detailed manual
          
        For complete documentation, run: %(prog)s --man
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global options
    parser.add_argument('--version', action='store_true',
                       help='show version information and exit')
    parser.add_argument('--man', action='store_true',
                       help='show detailed manual page and exit')
    parser.add_argument('--no-color', action='store_true',
                       help='disable colored output')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                       help='increase verbosity (-v, -vv, -vvv)')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='minimal output (errors only)')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='available commands')
    
    # Test command (default)
    test_parser = subparsers.add_parser('test', help='test URL accessibility')
    add_test_arguments(test_parser)
    
    # List command
    list_parser = subparsers.add_parser('list', help='list available data sources')
    add_list_arguments(list_parser)
    
    # Report command
    report_parser = subparsers.add_parser('report', help='generate reports from results')
    add_report_arguments(report_parser)
    
    # Add test arguments to main parser as well (for default behavior)
    add_test_arguments(parser)
    
    return parser

def add_test_arguments(parser):
    """Add arguments for the test command"""
    # Input sources (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--csv', '--file', metavar='FILE',
                           help='CSV file with URLs to test')
    input_group.add_argument('--url', metavar='URL',
                           help='single URL to test')
    input_group.add_argument('--sheet', metavar='URL',
                           help='Google Sheets CSV URL')
    input_group.add_argument('--cyber1', action='store_true',
                           help='test Cyber1 curriculum URLs')
    input_group.add_argument('--cyber2', action='store_true',
                           help='test Cyber2 curriculum URLs')
    input_group.add_argument('--cyber3', action='store_true',
                           help='test Cyber3 curriculum URLs')
    input_group.add_argument('--all-cyber', action='store_true',
                           help='test all cybersecurity curriculum URLs')
    
    # Test options
    parser.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT,
                       metavar='SECONDS', help=f'request timeout (default: {DEFAULT_TIMEOUT}s)')
    parser.add_argument('-j', '--parallel', type=int, default=1,
                       metavar='N', help='number of parallel tests (default: 1)')
    parser.add_argument('--no-https-upgrade', action='store_true',
                       help='disable automatic HTTP to HTTPS upgrade')
    parser.add_argument('--skip-youtube', action='store_true',
                       help='skip YouTube video availability checks')
    
    # Output options
    parser.add_argument('-o', '--output', metavar='FILE',
                       help='save results to file (JSON format)')
    parser.add_argument('--format', choices=['json', 'csv', 'text'], default='text',
                       help='output format (default: text)')
    parser.add_argument('--filter', choices=['all', 'blocked', 'accessible', 'warnings'],
                       default='all', help='filter results (default: all)')

def add_list_arguments(parser):
    """Add arguments for the list command"""
    parser.add_argument('--sources', action='store_true',
                       help='list predefined data sources')
    parser.add_argument('--formats', action='store_true',
                       help='list supported output formats')

def add_report_arguments(parser):
    """Add arguments for the report command"""
    parser.add_argument('input_file', metavar='RESULTS_FILE',
                       help='JSON results file to generate report from')
    parser.add_argument('-o', '--output', metavar='FILE',
                       help='output file (default: stdout)')
    parser.add_argument('--format', choices=['html', 'text', 'csv'],
                       default='html', help='report format (default: html)')
    parser.add_argument('--filter', choices=['all', 'blocked', 'accessible', 'warnings'],
                       default='all', help='filter results in report')

def show_manual():
    """Display the manual page"""
    manual = textwrap.dedent("""
    CAN I ACCESS?(1)                 User Commands                CAN I ACCESS?(1)
    
    NAME
           can-i-access - test educational website accessibility from school networks
    
    SYNOPSIS
           can-i-access [OPTIONS] [COMMAND]
           can-i-access --csv FILE [OPTIONS]
           can-i-access --url URL [OPTIONS]
           can-i-access --cyber1|--cyber2|--cyber3 [OPTIONS]
    
    DESCRIPTION
           Can I Access? is a command-line tool for testing whether educational
           websites are accessible from within school networks. It helps educators
           and IT administrators identify potential firewall blocks, connectivity
           issues, and security warnings for educational resources.
    
           The tool tests URLs using standard HTTP requests and provides detailed
           information about accessibility status, security warnings, and specific
           issues that might prevent access in educational environments.
    
    COMMANDS
           test        Test URL accessibility (default command)
           list        List available data sources and formats
           report      Generate reports from saved results
    
    INPUT SOURCES
           --csv FILE
                  Read URLs from a CSV file. The file must contain a column named
                  'URL'. Additional columns for site name, importance, unit, and
                  PII requirements are supported.
    
           --url URL
                  Test a single URL.
    
           --sheet URL
                  Fetch URLs from a published Google Sheets CSV.
    
           --cyber1, --cyber2, --cyber3
                  Use predefined cybersecurity curriculum URLs.
    
           --all-cyber
                  Test all predefined cybersecurity curriculum URLs.
    
    OPTIONS
           -t, --timeout SECONDS
                  Set request timeout in seconds (default: 10).
    
           -j, --parallel N
                  Run N parallel tests for faster processing (default: 1).
    
           --no-https-upgrade
                  Disable automatic HTTP to HTTPS upgrade attempts.
    
           --skip-youtube
                  Skip YouTube video availability checks.
    
           -o, --output FILE
                  Save results to file in JSON format for later analysis.
    
           --format FORMAT
                  Output format: json, csv, or text (default: text).
    
           --filter FILTER
                  Filter results: all, blocked, accessible, or warnings.
    
           -v, --verbose
                  Increase verbosity. Use multiple times for more detail.
    
           -q, --quiet
                  Minimal output (errors only).
    
           --no-color
                  Disable colored output.
    
           --version
                  Show version information.
    
           --man
                  Show this manual page.
    
    OUTPUT FORMATS
           The tool provides several output formats:
    
           text    Human-readable colored output with summaries
           json    Machine-readable JSON for automation
           csv     Comma-separated values for spreadsheet import
    
    EXIT STATUS
           0       All tests completed successfully
           1       Some URLs failed or had errors
           2       Invalid arguments or configuration
           3       Network or system error
    
    EXAMPLES
           Test default cybersecurity curriculum:
               can-i-access
    
           Test URLs from a CSV file with verbose output:
               can-i-access --csv school-websites.csv -v
    
           Test a single URL and save results:
               can-i-access --url https://example.com --output results.json
    
           Test only accessible URLs from Cyber1 curriculum:
               can-i-access --cyber1 --filter accessible
    
           Generate an HTML report from saved results:
               can-i-access report results.json --format html -o report.html
    
           Run parallel tests for faster processing:
               can-i-access --csv large-list.csv --parallel 5
    
    CSV FORMAT
           CSV files should contain at minimum a 'URL' column. Additional supported
           columns include:
    
           site                    Resource name
           unit                    Educational unit number
           reporting z-index       Importance ranking (higher = more important)
           Student PII Needed      Privacy flag (TRUE/FALSE)
    
    SECURITY
           This tool only performs read-only network tests and does not attempt
           to bypass security measures. It respects robots.txt, follows redirects
           appropriately, and uses standard HTTP methods.
    
           For YouTube videos, it uses the public oEmbed API to check availability
           without requiring authentication or API keys.
    
    AUTHOR
           Written by RiceC-at-MasonHS for educational technology assessment.
    
    REPORTING BUGS
           Report bugs to: https://github.com/RiceC-at-MasonHS/can-i-access/issues
    
    COPYRIGHT
           MIT License. Free software: you are free to change and redistribute it.
    
    SEE ALSO
           curl(1), wget(1), dig(1)
    
    Can I Access? 2.0                 July 2025                 CAN I ACCESS?(1)
    """)
    
    # Use pager if available
    try:
        import subprocess
        if sys.stdout.isatty():
            pager = os.environ.get('PAGER', 'less')
            if pager == 'less':
                pager_cmd = ['less', '-R']  # -R for color support
            else:
                pager_cmd = [pager]
            
            proc = subprocess.Popen(pager_cmd, stdin=subprocess.PIPE, text=True)
            proc.communicate(manual)
        else:
            print(manual)
    except:
        print(manual)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        eprint(f"\n{Colors.YELLOW}⚠ Interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        eprint(f"{Colors.RED}✗ Fatal error: {e}{Colors.END}")
        sys.exit(1)

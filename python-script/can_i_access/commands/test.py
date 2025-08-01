"""
Test command implementation - the main URL testing functionality
"""

import sys
import csv
import json
import time
import io
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from .. import check_url_accessibility, Colors, eprint, format_url_for_display, PREDEFINED_SHEETS

def run_test_command(args):
    """Execute the test command"""
    # Determine input source
    urls_to_test = []
    source_name = "Unknown"
    
    if args.url:
        urls_to_test = [{'url': args.url}]
        source_name = "Single URL"
    elif args.csv:
        urls_to_test, source_name = load_urls_from_csv(args.csv)
    elif args.sheet:
        urls_to_test, source_name = load_urls_from_sheet(args.sheet, "Custom Sheet")
    elif args.cyber1:
        urls_to_test, source_name = load_urls_from_sheet(PREDEFINED_SHEETS['cyber1'], "Cyber1")
    elif args.cyber2:
        urls_to_test, source_name = load_urls_from_sheet(PREDEFINED_SHEETS['cyber2'], "Cyber2")
    elif args.cyber3:
        urls_to_test, source_name = load_urls_from_sheet(PREDEFINED_SHEETS['cyber3'], "Cyber3")
    elif args.all_cyber:
        # Load all cybersecurity sheets
        urls_to_test = []
        for name, sheet_url in PREDEFINED_SHEETS.items():
            sheet_urls, _ = load_urls_from_sheet(sheet_url, name.title())
            for url_data in sheet_urls:
                url_data['source'] = name.title()
            urls_to_test.extend(sheet_urls)
        source_name = "All Cybersecurity Curricula"
    else:
        # Default: load cyber1
        urls_to_test, source_name = load_urls_from_sheet(PREDEFINED_SHEETS['cyber1'], "Cyber1 (default)")
    
    if not urls_to_test:
        eprint(f"{Colors.RED}✗ No URLs to test{Colors.END}")
        sys.exit(1)
    
    # Print header
    if not args.quiet:
        print(f"{Colors.BOLD}{Colors.BLUE}Can I Access? - Network Accessibility Test{Colors.END}")
        print(f"{Colors.CYAN}Source: {source_name}{Colors.END}")
        print(f"{Colors.CYAN}URLs to test: {len(urls_to_test)}{Colors.END}")
        print(f"{Colors.CYAN}Timeout: {args.timeout}s{Colors.END}")
        print()
    
    # Run tests
    results = []
    start_time = time.time()
    
    for i, url_data in enumerate(urls_to_test, 1):
        url = url_data['url'].strip()
        if not url:
            continue
            
        if not args.quiet:
            progress = f"[{i:3d}/{len(urls_to_test)}]"
            display_url = format_url_for_display(url, 50)
            print(f"{Colors.CYAN}{progress}{Colors.END} Testing: {display_url}")
        
        # Test the URL
        result = check_url_accessibility(
            url, 
            timeout=args.timeout, 
            verbose=(args.verbose > 1)
        )
        
        # Add metadata from CSV if available
        for key in ['site_name', 'unit', 'importance', 'pii_required']:
            if key in url_data:
                result[key] = url_data[key]
        
        result['source'] = url_data.get('source', source_name)
        results.append(result)
        
        # Show immediate result unless quiet
        if not args.quiet:
            status_color = get_status_color(result['status'])
            print(f"    → {status_color}{result['status']}{Colors.END}")
            if result['message'] and args.verbose:
                print(f"      {result['message']}")
        
        # Brief pause to avoid overwhelming the network
        if i < len(urls_to_test):
            time.sleep(0.1)
    
    total_time = time.time() - start_time
    
    # Filter results if requested
    if args.filter != 'all':
        results = filter_results(results, args.filter)
    
    # Output results
    if args.output:
        save_results(results, args.output, args.format)
        if not args.quiet:
            print(f"\n{Colors.GREEN}✓ Results saved to {args.output}{Colors.END}")
    
    # Print summary
    if not args.quiet:
        print_summary(results, total_time)
    
    # Exit with appropriate code
    failed_count = sum(1 for r in results if r['status'] in ['Not Reachable', 'Error', 'Video Removed'])
    sys.exit(1 if failed_count > 0 else 0)

def load_urls_from_csv(filename):
    """Load URLs from a CSV file"""
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
            # Detect CSV dialect
            sample = csvfile.read(1024)
            csvfile.seek(0)
            dialect = csv.Sniffer().sniff(sample)
            
            reader = csv.DictReader(csvfile, dialect=dialect)
            
            # Find URL column (case insensitive)
            url_column = None
            for field in reader.fieldnames:
                if field.lower().strip() == 'url':
                    url_column = field
                    break
            
            if not url_column:
                eprint(f"{Colors.RED}✗ CSV file must contain a 'URL' column{Colors.END}")
                eprint(f"Available columns: {', '.join(reader.fieldnames)}")
                sys.exit(2)
            
            for row_num, row in enumerate(reader, 2):
                url = row.get(url_column, '').strip()
                if url:
                    url_data = {'url': url}
                    
                    # Extract additional metadata if available
                    for csv_col, result_key in [
                        ('site', 'site_name'),
                        ('unit', 'unit'),
                        ('reporting z-index (higher, more important)', 'importance'),
                        ('Student PII Needed', 'pii_required')
                    ]:
                        if csv_col in row and row[csv_col]:
                            value = row[csv_col].strip()
                            if result_key == 'importance':
                                try:
                                    url_data[result_key] = int(value)
                                except ValueError:
                                    url_data[result_key] = 0
                            elif result_key == 'pii_required':
                                url_data[result_key] = value.upper() in ['TRUE', 'YES', '1']
                            else:
                                url_data[result_key] = value
                    
                    urls.append(url_data)
    
    except FileNotFoundError:
        eprint(f"{Colors.RED}✗ File not found: {filename}{Colors.END}")
        sys.exit(2)
    except Exception as e:
        eprint(f"{Colors.RED}✗ Error reading CSV: {e}{Colors.END}")
        sys.exit(2)
    
    return urls, f"CSV file ({filename})"

def load_urls_from_sheet(sheet_url, sheet_name):
    """Load URLs from a Google Sheets CSV"""
    urls = []
    try:
        req = Request(sheet_url, headers={
            'User-Agent': 'CanIAccess/2.0 (Educational Network Testing Tool)'
        })
        
        with urlopen(req, timeout=30) as response:
            csv_content = response.read().decode('utf-8')
        
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Find URL column
        url_column = None
        for field in reader.fieldnames:
            if field.lower().strip() == 'url':
                url_column = field
                break
        
        if not url_column:
            eprint(f"{Colors.RED}✗ Google Sheet must contain a 'URL' column{Colors.END}")
            sys.exit(2)
        
        for row in reader:
            url = row.get(url_column, '').strip()
            if url:
                url_data = {'url': url}
                
                # Extract metadata
                for csv_col, result_key in [
                    ('site', 'site_name'),
                    ('unit', 'unit'),
                    ('reporting z-index (higher, more important)', 'importance'),
                    ('Student PII Needed', 'pii_required')
                ]:
                    if csv_col in row and row[csv_col]:
                        value = row[csv_col].strip()
                        if result_key == 'importance':
                            try:
                                url_data[result_key] = int(value)
                            except ValueError:
                                url_data[result_key] = 0
                        elif result_key == 'pii_required':
                            url_data[result_key] = value.upper() in ['TRUE', 'YES', '1']
                        else:
                            url_data[result_key] = value
                
                urls.append(url_data)
    
    except Exception as e:
        eprint(f"{Colors.RED}✗ Error loading Google Sheet: {e}{Colors.END}")
        sys.exit(2)
    
    return urls, sheet_name

def filter_results(results, filter_type):
    """Filter results based on type"""
    if filter_type == 'blocked':
        return [r for r in results if r['status'] in ['Not Reachable', 'Video Removed']]
    elif filter_type == 'accessible':
        return [r for r in results if 'Accessible' in r['status'] or r['status'] == 'Reachable']
    elif filter_type == 'warnings':
        return [r for r in results if 'Warning' in r['status'] or 'HTTP' in r['status']]
    else:
        return results

def save_results(results, filename, format_type):
    """Save results to file"""
    try:
        if format_type == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': time.time(),
                    'results': results
                }, f, indent=2)
        elif format_type == 'csv':
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                if results:
                    writer = csv.DictWriter(f, fieldnames=results[0].keys())
                    writer.writeheader()
                    writer.writerows(results)
        else:  # text
            with open(filename, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"{result['url']}: {result['status']}\n")
    except Exception as e:
        eprint(f"{Colors.RED}✗ Error saving results: {e}{Colors.END}")
        sys.exit(2)

def get_status_color(status):
    """Get color for status"""
    if 'Accessible' in status or status == 'Reachable':
        return Colors.GREEN
    elif 'Warning' in status or 'HTTP' in status:
        return Colors.YELLOW
    elif status in ['Not Reachable', 'Video Removed', 'Error']:
        return Colors.RED
    else:
        return Colors.WHITE

def print_summary(results, total_time):
    """Print test summary"""
    total = len(results)
    if total == 0:
        return
    
    # Count by status
    accessible = sum(1 for r in results if 'Accessible' in r['status'] or r['status'] == 'Reachable')
    warnings = sum(1 for r in results if 'Warning' in r['status'])
    blocked = sum(1 for r in results if r['status'] in ['Not Reachable', 'Video Removed'])
    errors = sum(1 for r in results if r['status'] == 'Error')
    
    print(f"\n{Colors.BOLD}═══ SUMMARY ═══{Colors.END}")
    print(f"Total URLs tested: {Colors.BOLD}{total}{Colors.END}")
    print(f"Time taken: {Colors.BOLD}{total_time:.1f}s{Colors.END}")
    print()
    
    if accessible > 0:
        print(f"{Colors.GREEN}✓ Accessible: {accessible} ({accessible/total*100:.1f}%){Colors.END}")
    if warnings > 0:
        print(f"{Colors.YELLOW}⚠ Warnings: {warnings} ({warnings/total*100:.1f}%){Colors.END}")
    if blocked > 0:
        print(f"{Colors.RED}✗ Blocked/Unavailable: {blocked} ({blocked/total*100:.1f}%){Colors.END}")
    if errors > 0:
        print(f"{Colors.RED}⚠ Errors: {errors} ({errors/total*100:.1f}%){Colors.END}")
    
    # Show problematic URLs
    problem_results = [r for r in results if r['status'] in ['Not Reachable', 'Video Removed', 'Error']]
    if problem_results and len(problem_results) <= 10:
        print(f"\n{Colors.BOLD}Problematic URLs:{Colors.END}")
        for result in problem_results:
            status_color = get_status_color(result['status'])
            display_url = format_url_for_display(result['url'], 60)
            print(f"  {status_color}✗{Colors.END} {display_url}")
            print(f"    {result['message']}")
    elif len(problem_results) > 10:
        print(f"\n{Colors.YELLOW}⚠ {len(problem_results)} problematic URLs found. Use --output to save full results.{Colors.END}")
    
    # Success message
    if blocked == 0 and errors == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All URLs are accessible!{Colors.END}")
    elif blocked == 0:
        print(f"\n{Colors.YELLOW}✓ All URLs are reachable, but some have warnings{Colors.END}")

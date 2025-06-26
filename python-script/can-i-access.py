"""
`Can I Access? - School Network URL Accessibility Checker

This utility checks if educational websites are accessible from within your school's network.
Better to run than the web version, but requires Python and the `requests` library.

Usage:
    python url-check.py                    # Uses default Google Sheet
    python url-check.py --csv your_file.csv  # Uses local CSV file
    python url-check.py --sheet SHEET_URL    # Uses custom Google Sheet URL
    python url-check.py --cyber1              # Uses only Cyber1 sheet
    python url-check.py --cyber2              # Uses only Cyber2 sheet
    python url-check.py --cyber3              # Uses only Cyber3 sheet

GitHub: https://github.com/RiceC-at-MasonHS/can-i-access
"""
import csv
import sys
import argparse
import io

# Check for required dependencies with helpful error messages
try:
    import requests
except ImportError:
    print("=" * 60)
    print("❌ MISSING DEPENDENCY: 'requests' library not found")
    print("=" * 60)
    print("\nThis script requires the 'requests' library to check URL accessibility.")
    print("Please install it using one of these methods:\n")
    
    print("📦 Method 1 - Using pip (most common):")
    print("   pip install requests")
    print("   OR")
    print("   python -m pip install requests\n")
    
    print("📦 Method 2 - Using conda (if you have Anaconda/Miniconda):")
    print("   conda install requests\n")
    
    print("📦 Method 3 - If you're on a school computer with restrictions:")
    print("   pip install --user requests")
    print("   (This installs just for your user account)\n")
    
    print("💡 After installation, run this script again:")
    print(f"   python {sys.argv[0]}")
    print("\n" + "=" * 60)
    print("For more help, visit: https://requests.readthedocs.io/en/latest/user/install/")
    print("=" * 60)
    sys.exit(1)

# Default and predefined Google Sheet CSV URLs
DEFAULT_GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1W6139pV4zuGTrswAyaBSKD09eYDYjE4wKZsjKqueAEQ/pub?output=csv'

# Predefined sheet URLs for different categories
PREDEFINED_SHEETS = {
    'cyber1': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT9Oz-V5oBf5R0CTfGJl0BTnHf54zn0YEHKd6VvNYNWajK__z09mlyHmvH_6yjx4gpo319Ld4JgYxjY/pub?output=csv',  # Currently same as default
    'cyber2': 'https://docs.google.com/spreadsheets/d/PLACEHOLDER_CYBER2_SHEET_ID/pub?output=csv',  # TODO: Replace with actual sheet
    'cyber3': 'https://docs.google.com/spreadsheets/d/PLACEHOLDER_CYBER3_SHEET_ID/pub?output=csv'   # TODO: Replace with actual sheet
}

def find_url_column(fieldnames):
    """
    Find the URL column name regardless of case.
    
    Args:
        fieldnames (list): List of column names from CSV reader.
        
    Returns:
        str or None: The actual column name for URLs, or None if not found.
    """
    for field in fieldnames:
        if field.strip().lower() == 'url':
            return field
    return None

def check_url_reachability(url, timeout=10):
    """
    Checks if a given URL is reachable.

    Args:
        url (str): The URL to check.
        timeout (int): The maximum number of seconds to wait for a response.

    Returns:
        dict: A dictionary containing the URL, status, http_status, and message.
    """
    # Check if URL uses HTTP (insecure)
    is_http_only = url.lower().startswith('http://') and not url.lower().startswith('https://')
    
    try:
        # Add a User-Agent header to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Attempt to make a GET request to the URL
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Determine status based on HTTP vs HTTPS
        if is_http_only:
            status = "Reachable (HTTP Warning)"
            message = "⚠️ Site works but uses insecure HTTP. Modern browsers may block or show warnings. Consider requesting HTTPS version."
        else:
            status = "Reachable"
            message = "Successfully connected and received response."

        return {
            "url": url,
            "status": status,
            "http_status": response.status_code,
            "message": message,
            "is_http_only": is_http_only
        }
    except requests.exceptions.HTTPError as e:
        # HTTP error (e.g., 404 Not Found, 500 Internal Server Error)
        return {
            "url": url,
            "status": "Not Reachable",
            "http_status": e.response.status_code if e.response else "N/A",
            "message": f"HTTP Error: {e}",
            "is_http_only": is_http_only
        }
    except requests.exceptions.ConnectionError as e:
        # Network problem (e.g., DNS failure, refused connection, proxy issues)
        return {
            "url": url,            "status": "Not Reachable",
            "http_status": "N/A",
            "message": f"Connection Error: {e}. This could indicate network blocking.",
            "is_http_only": is_http_only
        }
    except requests.exceptions.Timeout as e:
        # Request timed out
        return {
            "url": url,
            "status": "Not Reachable",
            "http_status": "N/A",
            "message": f"Timeout Error: {e}. The site took too long to respond.",
            "is_http_only": is_http_only
        }
    except requests.exceptions.RequestException as e:
        # Any other requests-related error
        return {
            "url": url,
            "status": "Error",
            "http_status": "N/A",
            "message": f"An unexpected request error occurred: {e}",
            "is_http_only": is_http_only
        }
    except Exception as e:
        # General unexpected error
        return {
            "url": url,
            "status": "Error",
            "http_status": "N/A",
            "message": f"An unexpected error occurred: {e}",
            "is_http_only": is_http_only
        }

def process_multiple_sheets(sheet_urls, sheet_names=None):
    """
    Processes URLs from multiple Google Sheets and combines results.

    Args:
        sheet_urls (list): List of Google Sheet CSV URLs to process.
        sheet_names (list, optional): Names for each sheet for reporting.

    Returns:
        list: Combined list of dictionaries representing check results.
    """
    all_results = []
    
    if sheet_names is None:
        sheet_names = [f"Sheet {i+1}" for i in range(len(sheet_urls))]
    
    for i, sheet_url in enumerate(sheet_urls):
        sheet_name = sheet_names[i] if i < len(sheet_names) else f"Sheet {i+1}"
        print(f"\n{'='*60}")
        print(f"Processing {sheet_name}")
        print(f"{'='*60}")
        
        try:
            results = process_urls_from_google_sheet(sheet_url)
            # Add sheet identifier to each result
            for result in results:
                result['sheet_source'] = sheet_name
            all_results.extend(results)
            
        except SystemExit:
            # If process_urls_from_google_sheet fails, continue with other sheets
            print(f"Failed to process {sheet_name}, continuing with other sheets...")
            continue
    
    return all_results

def process_urls_from_google_sheet(sheet_url, sheet_name="Google Sheet"):
    """
    Fetches URLs from a Google Sheet published as CSV and checks their reachability.

    Args:
        sheet_url (str): The URL to the published Google Sheet CSV.
        sheet_name (str): Name of the sheet for reporting purposes.

    Returns:
        list: A list of dictionaries, each representing the check result for a URL.
    """
    results = []
    try:
        print(f"Fetching URLs from {sheet_name}: {sheet_url}")
        
        # Fetch the CSV data from Google Sheets
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(sheet_url, headers=headers, timeout=30)
        response.raise_for_status()
          # Parse the CSV content
        csv_content = response.text
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Find URL column (case insensitive)
        url_column = find_url_column(reader.fieldnames)
        if not url_column:
            print(f"Error: {sheet_name} must contain a column named 'URL' (case insensitive).", file=sys.stderr)
            print(f"Available columns: {', '.join(reader.fieldnames)}", file=sys.stderr)
            sys.exit(1)

        print(f"Processing URLs from {sheet_name}...")
        for row in reader:
            url = row[url_column].strip()
            if url:  # Only process if URL is not empty
                print(f"Checking: {url}")
                result = check_url_reachability(url)
                result['sheet_source'] = sheet_name  # Always add source
                results.append(result)
            else:
                results.append({
                    "url": f"Empty URL in {sheet_name}",
                    "status": "Skipped",
                    "http_status": "N/A",
                    "message": f"Empty URL found in {sheet_name} row.",
                    "sheet_source": sheet_name
                })
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {sheet_name}: {e}", file=sys.stderr)
        print(f"Please ensure {sheet_name} is published to the web as CSV.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing {sheet_name} data: {e}", file=sys.stderr)
        sys.exit(1)
        
    return results

def process_urls_from_csv(csv_filepath):
    """
    Reads URLs from a CSV file and checks their reachability.

    Args:
        csv_filepath (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, each representing the check result for a URL.
    """
    results = []
    try:
        with open(csv_filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Find URL column (case insensitive)
            url_column = find_url_column(reader.fieldnames)
            if not url_column:
                print("Error: CSV must contain a column named 'URL' (case insensitive).", file=sys.stderr)
                print(f"Available columns: {', '.join(reader.fieldnames)}", file=sys.stderr)
                sys.exit(1)

            print(f"Processing URLs from '{csv_filepath}'...")
            for row in reader:
                url = row[url_column].strip()
                if url: # Only process if URL is not empty
                    print(f"Checking: {url}")
                    result = check_url_reachability(url)
                    result['sheet_source'] = f"CSV File ({csv_filepath})"  # Add source
                    results.append(result)
                else:
                    results.append({
                        "url": "Empty URL in CSV",
                        "status": "Skipped",
                        "http_status": "N/A",
                        "message": "Empty URL found in CSV row.",
                        "sheet_source": f"CSV File ({csv_filepath})"
                    })
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}", file=sys.stderr)
        sys.exit(1)
    return results

def generate_report(results):
    """
    Generates a detailed HTML report from the URL check results.

    Args:
        results (list): A list of dictionaries, each representing the check result for a URL.

    Returns:
        str: The HTML formatted report with embedded CSS.
    """    # Calculate summary statistics
    reachable_count = sum(1 for r in results if r["status"] in ["Reachable", "Reachable (HTTP Warning)"])
    http_warning_count = sum(1 for r in results if r["status"] == "Reachable (HTTP Warning)")
    not_reachable_count = sum(1 for r in results if r["status"] == "Not Reachable")
    error_count = sum(1 for r in results if r["status"] == "Error")
    skipped_count = sum(1 for r in results if r["status"] == "Skipped")
    total_urls = len(results)
    
    # Generate breakdown by source
    sources = set(r.get("sheet_source", "Single Source") for r in results)
    has_multiple_sheets = len(sources) > 1 or any("sheet_source" in r for r in results)
    
    # HTML with embedded CSS
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Can I Access? - Network Accessibility Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            margin: 5px 0;
            opacity: 0.9;
            font-size: 1.3em;
            font-weight: 400;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.8;
            font-size: 1em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        
        .summary-card.success {{ border-left-color: #28a745; }}
        .summary-card.warning {{ border-left-color: #ffc107; }}
        .summary-card.danger {{ border-left-color: #dc3545; }}
        
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .summary-card .number {{
            font-size: 3em;
            font-weight: bold;
            margin: 0;
            line-height: 1;
        }}
        
        .summary-card.success .number {{ color: #28a745; }}
        .summary-card.warning .number {{ color: #ffc107; }}
        .summary-card.danger .number {{ color: #dc3545; }}
        .summary-card .number {{ color: #667eea; }}
        
        .breakdown {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .breakdown h2 {{
            color: #333;
            margin-top: 0;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .source-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .source-item:last-child {{ border-bottom: none; }}
        
        .source-name {{
            font-weight: bold;
            color: #333;
        }}
        
        .source-stats {{
            font-family: monospace;
            font-size: 1.1em;
            color: #666;
        }}
        
        .table-container {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .table-header {{
            background: #667eea;
            color: white;
            padding: 20px;
            margin: 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        
        th {{
            background-color: #f8f9fa;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #dee2e6;
        }}
        
        td {{
            padding: 12px 8px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .status {{
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
          .status.reachable {{
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        
        .status.reachable-http-warning {{
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }}
        
        .status.not-reachable {{
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .status.error {{
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }}
        
        .status.skipped {{
            background-color: #e2e3e5;
            color: #383d41;
            border: 1px solid #d6d8db;
        }}
        
        .url-cell {{
            max-width: 300px;
            word-break: break-all;
            font-family: monospace;
            font-size: 0.85em;
        }}
        
        .message-cell {{
            max-width: 400px;
            word-wrap: break-word;
        }}
        
        .http-status {{
            font-family: monospace;
            font-weight: bold;
            text-align: center;
        }}
        
        .footer {{
            text-align: center;
            color: #666;
            font-style: italic;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid #dee2e6;
        }}
        
        .no-data {{
            text-align: center;
            padding: 40px;
            color: #666;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .header h1 {{ font-size: 2em; }}
            .summary {{ grid-template-columns: 1fr; }}
            .table-container {{ overflow-x: auto; }}
            table {{ min-width: 600px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Can I Access?</h1>
        <div class="subtitle">School Network Accessibility Report</div>
        <p>Testing educational resource accessibility from within your school network</p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Total URLs</h3>
            <div class="number">{total_urls}</div>
        </div>
        <div class="summary-card success">
            <h3>Reachable</h3>
            <div class="number">{reachable_count}</div>
        </div>
        <div class="summary-card danger">
            <h3>Not Reachable</h3>
            <div class="number">{not_reachable_count}</div>
        </div>        <div class="summary-card warning">
            <h3>Errors</h3>
            <div class="number">{error_count}</div>
        </div>
        <div class="summary-card warning">
            <h3>HTTP Warnings</h3>
            <div class="number">{http_warning_count}</div>
        </div>
    </div>"""

    # Add source breakdown if multiple sources
    if has_multiple_sheets:
        html += """
    <div class="breakdown">
        <h2>📋 Breakdown by Source</h2>"""
        
        for source in sorted(sources):
            source_results = [r for r in results if r.get("sheet_source", "Single Source") == source]
            source_reachable = sum(1 for r in source_results if r["status"] == "Reachable")
            source_total = len(source_results)
            success_rate = (source_reachable / source_total * 100) if source_total > 0 else 0
            
            html += f"""
        <div class="source-item">
            <span class="source-name">{source}</span>
            <span class="source-stats">{source_reachable}/{source_total} reachable ({success_rate:.1f}%)</span>
        </div>"""
        
        html += """
    </div>"""

    # Add detailed results table
    if not results:
        html += """
    <div class="no-data">
        <h2>No Data Available</h2>
        <p>No URLs were processed or found in the data source.</p>
    </div>"""
    else:
        html += """
    <div class="table-container">
        <h2 class="table-header">🔍 Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>URL</th>"""
        
        if has_multiple_sheets:
            html += "<th>Source</th>"
            
        html += """
                    <th>Status</th>
                    <th>HTTP Code</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>"""
        
        for r in results:
            url = r["url"]
            status = r["status"]
            http_status = str(r["http_status"])
            message = r["message"].replace('<', '&lt;').replace('>', '&gt;').strip()
            source = r.get("sheet_source", "Unknown")
            
            # Determine status class for styling
            status_class = status.lower().replace(' ', '-')
            
            html += f"""
                <tr>
                    <td class="url-cell">{url}</td>"""
            
            if has_multiple_sheets:
                html += f"<td>{source}</td>"
                
            html += f"""
                    <td><span class="status {status_class}">{status}</span></td>
                    <td class="http-status">{http_status}</td>
                    <td class="message-cell">{message}</td>
                </tr>"""
        
        html += """
            </tbody>
        </table>
    </div>"""

    # Add footer
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html += f"""
    <div class="footer">
        <p>📝 Report generated by <strong>Can I Access?</strong> on {current_time}</p>
        <p>🏫 School network accessibility testing tool</p>
        <p>🔗 <a href="https://github.com/RiceC-at-MasonHS/can-i-access" style="color: #667eea;">GitHub Repository</a></p>
    </div>
</body>
</html>"""

    return html

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Check URL accessibility from school network",
        epilog="Examples:\n"
               "  python url-check.py                           # Use all default sheets (cyber1, cyber2, cyber3)\n"
               "  python url-check.py --csv urls.csv           # Use local CSV file\n"
               "  python url-check.py --cyber1                 # Use only cyber1 sheet\n"
               "  python url-check.py --cyber2                 # Use only cyber2 sheet\n"
               "  python url-check.py --cyber3                 # Use only cyber3 sheet\n"
               "  python url-check.py --sheet SHEET_URL        # Use custom Google Sheet",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--csv', '--file', 
                      help='Path to local CSV file with URLs')
    group.add_argument('--sheet', '--google-sheet',
                      help='Custom Google Sheet CSV URL (published to web)')
    group.add_argument('--cyber1', action='store_true',
                      help='Use only the Cyber1 Google Sheet')
    group.add_argument('--cyber2', action='store_true',
                      help='Use only the Cyber2 Google Sheet')
    group.add_argument('--cyber3', action='store_true',
                      help='Use only the Cyber3 Google Sheet')
    
    args = parser.parse_args()
    
    # Determine data source and process URLs
    if args.csv:
        print(f"Using local CSV file: {args.csv}")
        checked_urls = process_urls_from_csv(args.csv)
    elif args.sheet:
        print(f"Using custom Google Sheet: {args.sheet}")
        checked_urls = process_urls_from_google_sheet(args.sheet, "Custom Sheet")
    elif args.cyber1:
        print("Using Cyber1 Google Sheet...")
        print(f"Sheet URL: {PREDEFINED_SHEETS['cyber1']}")
        checked_urls = process_urls_from_google_sheet(PREDEFINED_SHEETS['cyber1'], "Cyber1")
    elif args.cyber2:
        print("Using Cyber2 Google Sheet...")
        print(f"Sheet URL: {PREDEFINED_SHEETS['cyber2']}")
        checked_urls = process_urls_from_google_sheet(PREDEFINED_SHEETS['cyber2'], "Cyber2")
    elif args.cyber3:
        print("Using Cyber3 Google Sheet...")
        print(f"Sheet URL: {PREDEFINED_SHEETS['cyber3']}")
        checked_urls = process_urls_from_google_sheet(PREDEFINED_SHEETS['cyber3'], "Cyber3")
    else:
        print("Using all default Google Sheets (cyber1, cyber2, cyber3)...")
        sheet_urls = [PREDEFINED_SHEETS['cyber1'], PREDEFINED_SHEETS['cyber2'], PREDEFINED_SHEETS['cyber3']]
        sheet_names = ['Cyber1', 'Cyber2', 'Cyber3']
        checked_urls = process_multiple_sheets(sheet_urls, sheet_names)

    # Generate the report
    final_report = generate_report(checked_urls)    # Output the report to a file
    output_filename = "can-i-access-report.html"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)
        print(f"\n📊 Report saved to '{output_filename}'")
        print(f"🌐 Open the file in your web browser to view the formatted report")
    except Exception as e:
        print(f"Error saving report to file: {e}", file=sys.stderr)

    print("\n--- Can I Access Script Finished ---")
    print(f"Total URLs processed: {len(checked_urls)}")
    
    # Print quick summary
    reachable = sum(1 for r in checked_urls if r["status"] == "Reachable")
    not_reachable = sum(1 for r in checked_urls if r["status"] == "Not Reachable")
    errors = sum(1 for r in checked_urls if r["status"] == "Error")
    
    print(f"Quick Summary: {reachable} reachable, {not_reachable} not reachable, {errors} errors")
    
    # List problematic URLs for quick attention
    problem_urls = [r for r in checked_urls if r["status"] in ["Not Reachable", "Error"]]
    
    if problem_urls:
        print(f"\n🚨 URLs Requiring Attention ({len(problem_urls)} total):")
        print("=" * 60)
        
        for result in problem_urls:
            url = result["url"]
            status = result["status"]
            source = result.get("sheet_source", "Unknown")
            message = result["message"]
            
            # Truncate URL if too long for terminal display
            display_url = url if len(url) <= 50 else url[:47] + "..."
            
            print(f"❌ {status.upper()}: {display_url}")
            if source != "Unknown":
                print(f"   Source: {source}")
            print(f"   Issue: {message}")
            print()
        
        print("💡 Tip: Check the HTML report for full details and recommendations")
    else:
        print("\n✅ Great news! All URLs are reachable from your network.")
    
    print(f"\n📄 Full report available in: {output_filename}")
    print(f"🔗 Can I Access GitHub: https://github.com/RiceC-at-MasonHS/can-i-access")

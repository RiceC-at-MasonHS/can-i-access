"""
Report command implementation - generate reports from saved results
"""

import sys
import json
import csv
import time
from datetime import datetime
from .. import Colors, eprint

def run_report_command(args):
    """Execute the report command"""
    # Load results from file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'results' in data:
                results = data['results']
                timestamp = data.get('timestamp', time.time())
            else:
                results = data
                timestamp = time.time()
    except FileNotFoundError:
        eprint(f"{Colors.RED}✗ Results file not found: {args.input_file}{Colors.END}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        eprint(f"{Colors.RED}✗ Invalid JSON in results file: {e}{Colors.END}")
        sys.exit(2)
    except Exception as e:
        eprint(f"{Colors.RED}✗ Error reading results file: {e}{Colors.END}")
        sys.exit(2)
    
    # Filter results if requested
    if args.filter != 'all':
        results = filter_results(results, args.filter)
    
    # Generate report
    if args.format == 'html':
        report = generate_html_report(results, timestamp)
    elif args.format == 'csv':
        report = generate_csv_report(results)
    else:  # text
        report = generate_text_report(results, timestamp)
    
    # Output report
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"{Colors.GREEN}✓ Report saved to {args.output}{Colors.END}")
        except Exception as e:
            eprint(f"{Colors.RED}✗ Error saving report: {e}{Colors.END}")
            sys.exit(2)
    else:
        print(report)

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

def generate_html_report(results, timestamp):
    """Generate HTML report"""
    report_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate statistics
    total = len(results)
    if total == 0:
        return "<html><body><h1>No results to report</h1></body></html>"
    
    accessible = sum(1 for r in results if 'Accessible' in r['status'] or r['status'] == 'Reachable')
    warnings = sum(1 for r in results if 'Warning' in r['status'])
    blocked = sum(1 for r in results if r['status'] in ['Not Reachable', 'Video Removed'])
    errors = sum(1 for r in results if r['status'] == 'Error')
    
    # Count PII-required resources if available
    pii_count = sum(1 for r in results if r.get('pii_required', False))
    
    # Count by importance if available
    high_priority = sum(1 for r in results if r.get('importance', 0) > 50)
    
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
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card.success {{ border-left: 4px solid #28a745; }}
        .summary-card.warning {{ border-left: 4px solid #ffc107; }}
        .summary-card.danger {{ border-left: 4px solid #dc3545; }}
        .summary-card.info {{ border-left: 4px solid #17a2b8; }}
        .number {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
        .success .number {{ color: #28a745; }}
        .warning .number {{ color: #ffc107; }}
        .danger .number {{ color: #dc3545; }}
        .info .number {{ color: #17a2b8; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        .status {{
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .status.accessible {{ background: #d4edda; color: #155724; }}
        .status.warning {{ background: #fff3cd; color: #856404; }}
        .status.blocked {{ background: #f8d7da; color: #721c24; }}
        .url-cell {{ font-family: monospace; word-break: break-all; max-width: 300px; }}
        .pii-indicator {{ color: #dc3545; font-weight: bold; }}
        .importance {{ font-weight: bold; }}
        .importance.high {{ color: #dc3545; }}
        .importance.medium {{ color: #ffc107; }}
        .importance.low {{ color: #28a745; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Can I Access? Network Report</h1>
        <p>Generated on {report_time}</p>
    </div>
    
    <div class="summary">
        <div class="summary-card info">
            <h3>Total URLs</h3>
            <div class="number">{total}</div>
        </div>
        <div class="summary-card success">
            <h3>Accessible</h3>
            <div class="number">{accessible}</div>
            <small>{(accessible/total*100):.1f}%</small>
        </div>
        <div class="summary-card warning">
            <h3>Warnings</h3>
            <div class="number">{warnings}</div>
            <small>{(warnings/total*100):.1f}%</small>
        </div>
        <div class="summary-card danger">
            <h3>Blocked</h3>
            <div class="number">{blocked}</div>
            <small>{(blocked/total*100):.1f}%</small>
        </div>"""
    
    if pii_count > 0:
        html += f"""
        <div class="summary-card info">
            <h3>PII Required</h3>
            <div class="number">{pii_count}</div>
            <small>{(pii_count/total*100):.1f}%</small>
        </div>"""
    
    if high_priority > 0:
        html += f"""
        <div class="summary-card warning">
            <h3>High Priority</h3>
            <div class="number">{high_priority}</div>
            <small>{(high_priority/total*100):.1f}%</small>
        </div>"""
    
    html += """
    </div>
    
    <table>
        <thead>
            <tr>
                <th>URL</th>
                <th>Status</th>"""
    
    # Add optional columns if data is available
    if any(r.get('site_name') for r in results):
        html += "<th>Site</th>"
    if any(r.get('unit') for r in results):
        html += "<th>Unit</th>"
    if any(r.get('importance') for r in results):
        html += "<th>Priority</th>"
    if any(r.get('pii_required') for r in results):
        html += "<th>PII</th>"
    
    html += """
                <th>Message</th>
            </tr>
        </thead>
        <tbody>"""
    
    for result in results:
        # Determine status class
        if 'Accessible' in result['status'] or result['status'] == 'Reachable':
            status_class = 'accessible'
        elif 'Warning' in result['status']:
            status_class = 'warning'
        else:
            status_class = 'blocked'
        
        html += f"""
            <tr>
                <td class="url-cell">{result['url']}</td>
                <td><span class="status {status_class}">{result['status']}</span></td>"""
        
        # Add optional columns
        if any(r.get('site_name') for r in results):
            html += f"<td>{result.get('site_name', '')}</td>"
        if any(r.get('unit') for r in results):
            html += f"<td>{result.get('unit', '')}</td>"
        if any(r.get('importance') for r in results):
            importance = result.get('importance', 0)
            if importance > 70:
                importance_class = 'high'
            elif importance > 30:
                importance_class = 'medium'
            else:
                importance_class = 'low'
            html += f"<td><span class=\"importance {importance_class}\">{importance}</span></td>"
        if any(r.get('pii_required') for r in results):
            pii_text = "YES" if result.get('pii_required', False) else "NO"
            pii_class = "pii-indicator" if result.get('pii_required', False) else ""
            html += f"<td><span class=\"{pii_class}\">{pii_text}</span></td>"
        
        html += f"""
                <td>{result['message']}</td>
            </tr>"""
    
    html += """
        </tbody>
    </table>
    
    <div style="text-align: center; margin-top: 30px; color: #666;">
        <p>Generated by Can I Access? v2.0 - Educational Network Testing Tool</p>
        <p><a href="https://github.com/RiceC-at-MasonHS/can-i-access">GitHub Repository</a></p>
    </div>
</body>
</html>"""
    
    return html

def generate_csv_report(results):
    """Generate CSV report"""
    if not results:
        return "No results to report"
    
    import io
    output = io.StringIO()
    
    # Determine all available fields
    fieldnames = set()
    for result in results:
        fieldnames.update(result.keys())
    
    # Order fields logically
    ordered_fields = ['url', 'status', 'http_status', 'message', 'site_name', 'unit', 'importance', 'pii_required', 'source', 'response_time']
    fieldnames = [f for f in ordered_fields if f in fieldnames] + [f for f in fieldnames if f not in ordered_fields]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)
    
    return output.getvalue()

def generate_text_report(results, timestamp):
    """Generate plain text report"""
    report_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    lines = []
    lines.append("Can I Access? - Network Accessibility Report")
    lines.append("=" * 50)
    lines.append(f"Generated: {report_time}")
    lines.append("")
    
    if not results:
        lines.append("No results to report")
        return "\\n".join(lines)
    
    # Summary
    total = len(results)
    accessible = sum(1 for r in results if 'Accessible' in r['status'] or r['status'] == 'Reachable')
    warnings = sum(1 for r in results if 'Warning' in r['status'])
    blocked = sum(1 for r in results if r['status'] in ['Not Reachable', 'Video Removed'])
    errors = sum(1 for r in results if r['status'] == 'Error')
    
    lines.append("SUMMARY")
    lines.append("-" * 20)
    lines.append(f"Total URLs tested: {total}")
    lines.append(f"Accessible: {accessible} ({accessible/total*100:.1f}%)")
    lines.append(f"Warnings: {warnings} ({warnings/total*100:.1f}%)")
    lines.append(f"Blocked: {blocked} ({blocked/total*100:.1f}%)")
    lines.append(f"Errors: {errors} ({errors/total*100:.1f}%)")
    lines.append("")
    
    # Detailed results
    lines.append("DETAILED RESULTS")
    lines.append("-" * 20)
    
    for result in results:
        lines.append(f"URL: {result['url']}")
        lines.append(f"Status: {result['status']}")
        if result.get('site_name'):
            lines.append(f"Site: {result['site_name']}")
        if result.get('unit'):
            lines.append(f"Unit: {result['unit']}")
        if result.get('importance'):
            lines.append(f"Priority: {result['importance']}")
        if result.get('pii_required'):
            lines.append(f"PII Required: {'YES' if result['pii_required'] else 'NO'}")
        lines.append(f"Message: {result['message']}")
        lines.append("")
    
    return "\\n".join(lines)

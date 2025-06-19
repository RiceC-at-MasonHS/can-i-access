"""
This utility is better to run than the web-version. 
But you need to have Python installed on your computer, and the `requests` library.
"""
import csv
import requests
import sys

def check_url_reachability(url, timeout=10):
    """
    Checks if a given URL is reachable.

    Args:
        url (str): The URL to check.
        timeout (int): The maximum number of seconds to wait for a response.

    Returns:
        dict: A dictionary containing the URL, status, http_status, and message.
    """
    try:
        # Add a User-Agent header to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Attempt to make a GET request to the URL
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        return {
            "url": url,
            "status": "Reachable",
            "http_status": response.status_code,
            "message": "Successfully connected and received response."
        }
    except requests.exceptions.HTTPError as e:
        # HTTP error (e.g., 404 Not Found, 500 Internal Server Error)
        return {
            "url": url,
            "status": "Not Reachable",
            "http_status": e.response.status_code if e.response else "N/A",
            "message": f"HTTP Error: {e}"
        }
    except requests.exceptions.ConnectionError as e:
        # Network problem (e.g., DNS failure, refused connection, proxy issues)
        return {
            "url": url,
            "status": "Not Reachable",
            "http_status": "N/A",
            "message": f"Connection Error: {e}. This could indicate network blocking."
        }
    except requests.exceptions.Timeout as e:
        # Request timed out
        return {
            "url": url,
            "status": "Not Reachable",
            "http_status": "N/A",
            "message": f"Timeout Error: {e}. The site took too long to respond."
        }
    except requests.exceptions.RequestException as e:
        # Any other requests-related error
        return {
            "url": url,
            "status": "Error",
            "http_status": "N/A",
            "message": f"An unexpected request error occurred: {e}"
        }
    except Exception as e:
        # General unexpected error
        return {
            "url": url,
            "status": "Error",
            "http_status": "N/A",
            "message": f"An unexpected error occurred: {e}"
        }

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
            if 'URL' not in reader.fieldnames:
                print("Error: CSV must contain a column named 'URL'.", file=sys.stderr)
                sys.exit(1)

            print(f"Processing URLs from '{csv_filepath}'...")
            for row in reader:
                url = row['URL'].strip()
                if url: # Only process if URL is not empty
                    print(f"Checking: {url}")
                    result = check_url_reachability(url)
                    results.append(result)
                else:
                    results.append({
                        "url": "Empty URL in CSV",
                        "status": "Skipped",
                        "http_status": "N/A",
                        "message": "Empty URL found in CSV row."
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
    Generates a detailed Markdown report from the URL check results.

    Args:
        results (list): A list of dictionaries, each representing the check result for a URL.

    Returns:
        str: The Markdown formatted report.
    """
    report = "# School Network URL Reachability Report\n\n"
    report += "This report details the reachability of various web resources from within the school's network. "
    report += "Please review the 'Status' and 'Message' columns, especially for URLs marked 'Not Reachable' "
    report += "or 'Error', as these may indicate network blocking or connectivity issues. "
    report += "The HTTP Status Code provides additional context for successful connections or server-side errors.\n\n"

    report += "## Summary of Results\n"
    reachable_count = sum(1 for r in results if r["status"] == "Reachable")
    not_reachable_count = sum(1 for r in results if r["status"] == "Not Reachable")
    error_count = sum(1 for r in results if r["status"] == "Error")
    skipped_count = sum(1 for r in results if r["status"] == "Skipped")
    total_urls = len(results)

    report += f"- Total URLs processed: {total_urls}\n"
    report += f"- Reachable URLs: {reachable_count}\n"
    report += f"- Not Reachable URLs: {not_reachable_count}\n"
    report += f"- URLs with Errors: {error_count}\n"
    report += f"- Skipped (Empty) URLs: {skipped_count}\n\n"

    report += "## Detailed Results\n\n"
    if not results:
        report += "No URLs were processed or found in the CSV.\n"
        return report

    report += "| URL | Status | HTTP Status Code | Message |\n"
    report += "|-----|--------|------------------|---------|\n"

    for r in results:
        url = r["url"]
        status = r["status"]
        http_status = str(r["http_status"])
        message = r["message"].replace('\n', ' ').strip() # Sanitize message for single line

        report += f"| {url} | {status} | {http_status} | {message} |\n"

    report += "\n---\n"
    report += "Report generated by the URL Reachability Checker Script."
    return report

if __name__ == "__main__":
    # Define the input CSV file path.
    # IMPORTANT: Replace 'your_urls.csv' with the actual path to your CSV file.
    csv_file_path = 'your_urls.csv'

    # Process the URLs
    checked_urls = process_urls_from_csv(csv_file_path)

    # Generate the report
    final_report = generate_report(checked_urls)

    # Output the report to a file
    output_filename = "url_reachability_report.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)
        print(f"\nReport saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving report to file: {e}", file=sys.stderr)

    print("\n--- Script Finished ---")

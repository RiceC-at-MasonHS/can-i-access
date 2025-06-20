document.addEventListener('DOMContentLoaded', () => {
    const csvFile = document.getElementById('csvFile');
    const urlInput = document.getElementById('urlInput');
    const checkButton = document.getElementById('checkButton');
    const loadGoogleSheetButton = document.getElementById('loadGoogleSheetButton');
    const corsHelpButton = document.getElementById('corsHelpButton');
    const clearButton = document.getElementById('clearButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const reportContainer = document.getElementById('reportContainer');    // IMPORTANT: Replace this with the actual URL of your Google Sheet published as CSV.
    // How to get this URL:
    // 1. Open your Google Sheet.
    // 2. Go to File > Share > Publish to web.
    // 3. Under the "Link" tab, select the sheet you want to publish.
    // 4. For "Publish as:", choose "Comma-separated values (.csv)".
    // 5. Copy the generated URL. It will look something like:
    //    https://docs.google.com/spreadsheets/d/e/2PACX-1vR-random-string-here/pub?output=csv
    const DEFAULT_GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/1W6139pV4zuGTrswAyaBSKD09eYDYjE4wKZsjKqueAEQ/pub?output=csv';

    /**
     * Parses CSV content and extracts URLs from the 'URL' column.
     * @param {string} text - The raw CSV string content.
     * @returns {string[]} An array of URLs.
     */
    function parseCSV(text) {
        const lines = text.split(/\r?\n/).filter(line => line.trim() !== '');
        if (lines.length === 0) return [];

        const headers = lines[0].split(',').map(h => h.trim());
        const urlColumnIndex = headers.findIndex(h => h.toLowerCase() === 'url');

        if (urlColumnIndex === -1) {
            displayMessage('Error: CSV file must contain a column named "URL".', 'error');
            return [];
        }

        const urls = [];
        for (let i = 1; i < lines.length; i++) {
            const columns = lines[i].split(',');
            if (columns[urlColumnIndex]) {
                urls.push(columns[urlColumnIndex].trim());
            }
        }
        return urls;
    }

    /**
     * Parses URLs from a textarea, one per line.
     * @param {string} text - The raw text content from the textarea.
     * @returns {string[]} An array of URLs.
     */    function parseTextArea(text) {
        return text.split(/\r?\n/).map(url => url.trim()).filter(url => url !== '');
    }

    /**
     * Gets the appropriate CSS class for a status value.
     * @param {string} status - The status string.
     * @returns {string} The CSS class name.
     */
    function getStatusClass(status) {
        if (status.includes('HTTP Warning')) {
            return 'status-http-warning';
        } else if (status === 'Fully Accessible' || status === 'Partially Accessible' || 
                   status === 'Reachable' || status === 'Likely Reachable' || status === 'Possibly Reachable') {
            return 'status-reachable';
        } else if (status === 'Not Reachable') {
            return 'status-not-reachable';
        } else if (status === 'Error') {
            return 'status-error';
        } else {
            return 'status-skipped';
        }
    }/**
     * Checks the reachability of a given URL using progressive testing methods from within the school network.
     * @param {string} url - The URL to check.
     * @param {number} timeout - The maximum number of milliseconds to wait for a response.
     * @returns {Promise<object>} A promise that resolves to an object containing URL check results.
     */    async function checkUrl(url, timeout = 10000) {
        const result = {
            url: url,
            status: "Error",
            http_status: "N/A",
            message: "An unexpected error occurred.",
            method: "Unknown",
            details: [],
            isHttpOnly: false
        };

        // Check if URL uses HTTP (insecure)
        result.isHttpOnly = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://');

        // Add detailed logging function
        const addLog = (step, success, details) => {
            result.details.push(`${step}: ${success ? '✓' : '✗'} ${details}`);
        };

        addLog("Starting connectivity test", true, "Testing from school network");

        // Check for HTTP-only URLs early
        if (result.isHttpOnly) {
            addLog("Security check", false, "⚠️ HTTP-only URL detected - browsers may block or show warnings");
        }

        // Method 1: Try favicon loading technique for basic connectivity
        try {
            addLog("Favicon test", true, "Attempting to load favicon.ico");
            const faviconResult = await new Promise((resolve) => {
                const img = new Image();
                const timeout_id = setTimeout(() => {
                    img.onload = img.onerror = null;
                    resolve({ success: false, reason: "timeout" });
                }, timeout);

                img.onload = () => {
                    clearTimeout(timeout_id);
                    resolve({ success: true, reason: "loaded" });
                };
                
                img.onerror = () => {
                    clearTimeout(timeout_id);
                    resolve({ success: true, reason: "error_but_reachable" });
                };

                try {
                    const urlObj = new URL(url);
                    img.src = `${urlObj.protocol}//${urlObj.host}/favicon.ico?_=${Date.now()}`;
                } catch (e) {
                    resolve({ success: false, reason: "invalid_url" });
                }
            });

            if (faviconResult.success) {
                addLog("Favicon test", true, `Domain reachable (${faviconResult.reason})`);
                
                // Method 1b: If favicon works, try full content load
                addLog("Full content test", true, "Attempting full page load");
                try {
                    const controller = new AbortController();
                    const id = setTimeout(() => controller.abort(), timeout);

                    const response = await fetch(url, {
                        method: 'GET',
                        mode: 'no-cors',
                        signal: controller.signal
                    });
                    clearTimeout(id);                    if (response) {
                        addLog("Full content test", true, "Page load completed successfully");
                        if (result.isHttpOnly) {
                            result.status = "Fully Accessible (HTTP Warning)";
                            result.message = "⚠️ Site accessible but uses insecure HTTP. Modern browsers may block or show warnings.";
                        } else {
                            result.status = "Fully Accessible";
                            result.message = "Site fully accessible from school network";
                        }
                        result.http_status = "200 (inferred)";
                        result.method = "Full Load + Favicon";
                        return result;
                    }
                } catch (fetchError) {
                    addLog("Full content test", false, `Failed: ${fetchError.message}`);
                }                // Fallback: Favicon worked but full load didn't
                if (result.isHttpOnly) {
                    result.status = "Partially Accessible (HTTP Warning)";
                    result.message = "⚠️ Domain reachable but uses insecure HTTP. Full content may be restricted and browsers may show warnings.";
                } else {
                    result.status = "Partially Accessible";
                    result.message = "Domain reachable but full content may be restricted";
                }
                result.http_status = "Favicon OK";
                result.method = "Favicon Only";
                return result;
            } else {
                addLog("Favicon test", false, `Failed: ${faviconResult.reason}`);
            }
        } catch (e) {
            addLog("Favicon test", false, `Exception: ${e.message}`);
        }

        // Method 2: Try direct no-cors fetch
        addLog("Direct fetch test", true, "Attempting no-CORS fetch");
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout);

        try {
            const response = await fetch(url, {
                method: 'GET',
                mode: 'no-cors',
                signal: controller.signal
            });
            clearTimeout(id);            if (response) {
                addLog("Direct fetch test", true, "Request completed");
                if (result.isHttpOnly) {
                    result.status = "Possibly Reachable (HTTP Warning)";
                    result.message = "⚠️ Request completed but uses insecure HTTP. Modern browsers may block or show warnings.";
                } else {
                    result.status = "Possibly Reachable";
                    result.message = "Request completed from school network (limited info due to CORS)";
                }
                result.http_status = "No-CORS Response";
                result.method = "No-CORS Fetch";
            } else {
                addLog("Direct fetch test", false, "No response received");
                result.status = "Not Reachable";
                result.http_status = "N/A";
                result.message = "No response from school network";
                result.method = "No-CORS Fetch";
            }        } catch (e) {
            clearTimeout(id);
            addLog("Direct fetch test", false, `Exception: ${e.message}`);
            result.status = "Not Reachable";
            result.http_status = "N/A";
            result.method = "No-CORS Fetch";
            if (e.name === 'AbortError') {
                result.message = "Timeout: Site took too long to respond from school network";
            } else if (e instanceof TypeError) {
                result.message = `Network blocked: ${e.message}. Site may be blocked by school firewall`;
            } else {
                result.message = `Connection failed: ${e.message}`;
            }
        }

        addLog("Test complete", true, `Final status: ${result.status}`);
        return result;
    }

    /**
     * Displays a message on the report container.
     * @param {string} msg - The message to display.
     * @param {'info'|'error'} type - The type of message (influences styling).
     */
    function displayMessage(msg, type = 'info') {
        const msgDiv = document.createElement('div');
        msgDiv.className = `p-4 mb-4 rounded-lg text-sm ${type === 'error' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`;
        msgDiv.textContent = msg;
        reportContainer.prepend(msgDiv); // Add to top of report
    }

    /**
     * Generates and displays the detailed URL reachability report.
     * @param {string[]} urls - An array of URLs to check.
     */
    async function generateReport(urls) {
        reportContainer.innerHTML = ''; // Clear previous report
        loadingIndicator.classList.remove('hidden'); // Show loading indicator

        if (urls.length === 0) {
            displayMessage('No URLs found to check. Please upload a CSV or paste URLs.', 'info');
            loadingIndicator.classList.add('hidden');
            return;
        }

        // Clear any existing input values to avoid confusion
        csvFile.value = '';
        urlInput.value = '';

        const results = [];
        // Process URLs one by one to show progress
        for (let i = 0; i < urls.length; i++) {
            const url = urls[i];
            // Skip if the URL is empty or just whitespace
            if (!url || url.trim() === '') {
                results.push({
                    url: "Empty URL",
                    status: "Skipped",
                    http_status: "N/A",
                    message: "URL was empty or whitespace."
                });
                continue;
            }            const result = await checkUrl(url);
            results.push(result);
            
            // Provide detailed real-time feedback
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = 'bg-gray-50 border-l-4 border-blue-400 p-3 mb-2 text-sm';
            
            const statusColor = result.status === 'Fully Accessible' || result.status === 'Partially Accessible' ? 'text-green-700' : 
                               result.status === 'Possibly Reachable' ? 'text-yellow-700' : 'text-red-700';
            
            const truncatedUrl = truncateUrl(url, 60);
            feedbackDiv.innerHTML = `
                <div class="font-medium text-gray-900">
                    [${i + 1}/${urls.length}] Testing: <span class="font-mono">${truncatedUrl}</span>
                </div>
                <div class="mt-1">
                    <span class="font-semibold ${statusColor}">Status: ${result.status}</span>
                    <span class="text-gray-600 ml-2">Method: ${result.method}</span>
                </div>
                ${result.details && result.details.length > 0 ? `
                <div class="mt-1 text-xs text-gray-500">
                    <div class="font-medium">Test Details:</div>
                    ${result.details.slice(-3).map(detail => `<div class="ml-2">• ${detail}</div>`).join('')}
                </div>
                ` : ''}
            `;
            reportContainer.prepend(feedbackDiv);
        }

        loadingIndicator.classList.add('hidden'); // Hide loading indicator        // Generate summary
        let reachableCount = 0;
        let httpWarningCount = 0;
        let notReachableCount = 0;
        let errorCount = 0;
        let skippedCount = 0;

        results.forEach(r => {
            if (r.status.includes("HTTP Warning")) {
                httpWarningCount++;
                reachableCount++; // HTTP warnings are still reachable
            } else if (r.status === "Fully Accessible" || r.status === "Partially Accessible" || r.status === "Reachable" || r.status === "Likely Reachable" || r.status === "Possibly Reachable") {
                reachableCount++;
            } else if (r.status === "Not Reachable" || r.status === "Blocked") {
                notReachableCount++;
            } else if (r.status === "Error") {
                errorCount++;
            } else if (r.status === "Skipped") {
                skippedCount++;
            }
        });        const totalUrls = results.length; // Use results.length to account for skipped

        let summaryHtml = `
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Summary of Results</h2>
            <ul class="list-disc list-inside text-gray-700 mb-6">
                <li>Total URLs processed: ${totalUrls}</li>
                <li>Reachable URLs: <span class="text-green-700 font-semibold">${reachableCount}</span></li>
                ${httpWarningCount > 0 ? `<li>URLs with HTTP Warnings: <span class="text-amber-700 font-semibold">${httpWarningCount}</span> ⚠️</li>` : ''}
                <li>Not Reachable URLs: <span class="text-red-700 font-semibold">${notReachableCount}</span></li>
                <li>URLs with Errors: <span class="text-orange-700 font-semibold">${errorCount}</span></li>
                <li>Skipped (Empty) URLs: <span class="text-gray-500 font-semibold">${skippedCount}</span></li>
            </ul>
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Detailed Results</h2>
        `;
        // Set innerHTML for summary, then append table
        reportContainer.innerHTML = summaryHtml;        // Generate detailed table
        if (results.length > 0) {
            const tableHtml = `
                <div class="table-container">
                    <table class="results-table divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tl-lg">URL</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">HTTP Status</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tr-lg">Details</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            ${results.map(r => {
                                const truncated = truncateUrl(r.url);
                                const needsTooltip = truncated !== r.url;
                                return `
                                <tr>
                                    <td class="px-6 py-4 text-sm font-medium text-gray-900 table-cell-url">
                                        <div class="group relative">
                                            <span class="${needsTooltip ? 'url-truncated' : ''}" 
                                                  ${needsTooltip ? `onmouseover="showTooltip(event, '${r.url.replace(/'/g, '\\\'')}')" onmouseout="hideTooltip()"` : ''}>
                                                ${truncated}
                                            </span>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 text-sm ${getStatusClass(r.status)}">${r.status}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-xs text-blue-600 font-mono">${r.method || 'N/A'}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${r.http_status}</td>
                                    <td class="px-6 py-4 text-sm text-gray-500 table-cell-message">${r.message}</td>                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        ${r.details && r.details.length > 0 ? 
                                            `<button onclick="showDetailedLogs(${JSON.stringify(r).replace(/"/g, '&quot;')}, '${r.url.replace(/'/g, '\\\'')}')" 
                                             class="text-blue-600 hover:text-blue-800 underline text-xs block mb-1">
                                                View Logs
                                             </button>` : 
                                            '<span class="text-gray-400 text-xs block mb-1">No logs</span>'
                                        }${!r.status.includes('Fully Accessible') && r.status !== 'Skipped' ? 
                                            `<button onclick="testManualAccess('${r.url.replace(/'/g, '\\\'')}')" 
                                             class="manual-test-btn hover:bg-yellow-600 text-white text-xs px-2 py-1 rounded block">
                                                ${r.status.includes('Partially Accessible') ? 'Test Full Access' : 
                                                  r.status.includes('Possibly Reachable') ? 'Verify Access' : 
                                                  r.status === 'Not Reachable' ? 'Retry Test' : 'Manual Check'}
                                             </button>` : ''
                                        }
                                    </td>
                                </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            reportContainer.innerHTML += tableHtml;
        } else {
            reportContainer.innerHTML += `<p class="text-gray-600">No detailed results to display.</p>`;
        }
    }    /**
     * Truncates a URL for display while preserving important parts
     * @param {string} url - The URL to truncate
     * @param {number} maxLength - Maximum length for the truncated URL
     * @returns {string} Truncated URL
     */
    function truncateUrl(url, maxLength = 120) {
        if (!url || url.length <= maxLength) {
            return url;
        }

        try {
            const urlObj = new URL(url);
            const protocol = urlObj.protocol;
            const domain = urlObj.hostname;
            const path = urlObj.pathname;
            const search = urlObj.search;
            const hash = urlObj.hash;
            
            // Build base URL
            const baseUrl = `${protocol}//${domain}`;
            
            // If just the domain + protocol is too long, truncate the domain
            if (baseUrl.length > maxLength - 3) {
                const availableForDomain = maxLength - protocol.length - 5; // -5 for "//..."
                return `${protocol}//${domain.substring(0, availableForDomain)}...`;
            }
            
            // Calculate remaining space for path and query
            const remainingSpace = maxLength - baseUrl.length - 3; // -3 for "..."
            
            // If we have a path or query parameters
            if (path !== '/' || search || hash) {
                const pathAndQuery = path + search + hash;
                
                if (pathAndQuery.length <= remainingSpace) {
                    return url; // No truncation needed
                }
                
                // Truncate path intelligently
                if (remainingSpace > 8) {
                    // Try to keep some path structure visible
                    const pathParts = path.split('/').filter(p => p);
                    let truncatedPath = '';
                    
                    if (pathParts.length > 0) {
                        // Keep first path segment if it fits
                        const firstSegment = '/' + pathParts[0];
                        if (firstSegment.length + search.length <= remainingSpace - 3) {
                            truncatedPath = firstSegment + '/...';
                            if (search) truncatedPath += search;
                        } else {
                            truncatedPath = path.substring(0, remainingSpace - search.length - 3) + '...';
                            if (search.length < remainingSpace - 3) truncatedPath += search;
                        }
                    } else {
                        truncatedPath = '...';
                    }
                    
                    return `${baseUrl}${truncatedPath}`;
                } else {
                    return `${baseUrl}...`;
                }
            }
            
            return baseUrl;
        } catch (e) {
            // If URL parsing fails, just truncate from the end
            return url.substring(0, maxLength - 3) + '...';
        }
    }

    // Event listener for the Check button
    checkButton.addEventListener('click', async () => {
        let urls = [];
        // Prioritize CSV upload
        if (csvFile.files.length > 0) {
            const file = csvFile.files[0];
            const reader = new FileReader();
            reader.onload = async (e) => {
                const text = e.target.result;
                urls = parseCSV(text);
                await generateReport(urls);
            };
            reader.onerror = () => {
                displayMessage('Error reading CSV file.', 'error');
                loadingIndicator.classList.add('hidden');
            };
            reader.readAsText(file);
        } else {
            // Fallback to textarea if no CSV is uploaded
            urls = parseTextArea(urlInput.value);
            await generateReport(urls);
        }
    });

    // Event listener for the new "Load Default URLs (Google Sheet)" button
    loadGoogleSheetButton.addEventListener('click', async () => {
        loadingIndicator.classList.remove('hidden');
        reportContainer.innerHTML = ''; // Clear existing report
        displayMessage('Attempting to load URLs from Google Sheet...', 'info');

        try {
            const response = await fetch(DEFAULT_GOOGLE_SHEET_CSV_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const csvText = await response.text();
            const urls = parseCSV(csvText);
            await generateReport(urls);
        } catch (error) {
            displayMessage(`Error loading Google Sheet CSV: ${error.message}. Make sure the sheet is published to web as CSV and CORS allows access.`, 'error');
            loadingIndicator.classList.add('hidden');
        }
    });

    /**
     * Shows a comprehensive help dialog about CORS issues and solutions
     */
    function showCorsHelp() {
        const helpContent = `
            <div class="bg-white rounded-lg shadow-xl max-w-4xl mx-auto p-6">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">School Network Testing Guide</h2>
                
                <div class="space-y-6">                    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                        <h3 class="text-lg font-semibold text-yellow-800 mb-2">What does this tool test?</h3>
                        <p class="text-yellow-700">This tool tests if websites are accessible from within your school's network. It checks if your school's internet connection and firewall allow access to educational resources that teachers and students need.</p>
                    </div>                    <div class="bg-green-50 border-l-4 border-green-400 p-4">
                        <h3 class="text-lg font-semibold text-green-800 mb-2">Getting Definitive Results:</h3>
                        <ol class="list-decimal list-inside text-green-700 space-y-2">
                            <li><strong>Manual Testing (Recommended):</strong>
                                <ul class="list-disc list-inside ml-4 mt-1">
                                    <li>Use the "Manual Test" buttons for uncertain results</li>
                                    <li>View sites directly in iframe testing modal</li>
                                    <li>Get real-world confirmation of accessibility</li>
                                </ul>
                            </li>
                            <li><strong>Direct Browser Testing:</strong> Open suspected URLs in new browser tabs</li>
                            <li><strong>Network Team Coordination:</strong> Share results with your school's IT team for policy adjustments</li>
                        </ol>
                    </div>                    <div class="bg-blue-50 border-l-4 border-blue-400 p-4">
                        <h3 class="text-lg font-semibold text-blue-800 mb-2">How This Tool Works:</h3>
                        <ul class="list-disc list-inside text-blue-700 space-y-1">
                            <li>Tests connectivity directly from your school's network</li>
                            <li>Uses favicon loading to check if domains are reachable</li>
                            <li>Attempts direct connections respecting school firewall rules</li>
                            <li>Provides manual testing for uncertain results</li>
                            <li>Shows which testing method provided each result</li>
                        </ul>
                    </div>

                    <div class="bg-purple-50 border-l-4 border-purple-400 p-4">
                        <h3 class="text-lg font-semibold text-purple-800 mb-2">Understanding Results:</h3>
                        <ul class="list-disc list-inside text-purple-700 space-y-1">
                            <li><strong>Reachable:</strong> Site is accessible from school network</li>
                            <li><strong>Possibly Reachable:</strong> Connection attempted but CORS limits details</li>
                            <li><strong>Not Reachable:</strong> Site appears blocked or unavailable from school</li>
                            <li><strong>Timeout:</strong> Site is very slow or partially blocked</li>
                        </ul>
                    </div>
                </div>

                <div class="mt-6 flex justify-center">
                    <button onclick="this.closest('.fixed').remove()" class="btn-primary">
                        Got it, thanks!
                    </button>
                </div>
            </div>
        `;

        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50';
        modal.innerHTML = `
            <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
                ${helpContent}
            </div>
        `;

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        document.body.appendChild(modal);
    }

    // Event listener for the CORS Help button
    corsHelpButton.addEventListener('click', showCorsHelp);

    // Event listener for the Clear Report button
    clearButton.addEventListener('click', () => {
        reportContainer.innerHTML = '';
        csvFile.value = ''; // Clear file input
        urlInput.value = ''; // Clear textarea
        loadingIndicator.classList.add('hidden');
    });
});

/**
 * Global tooltip element for URL display
 */
let tooltipElement = null;

/**
 * Shows a tooltip with the full URL at the cursor position
 * @param {Event} event - The mouse event
 * @param {string} fullUrl - The complete URL to display
 */
function showTooltip(event, fullUrl) {
    // Remove any existing tooltip
    hideTooltip();
    
    // Create tooltip element
    tooltipElement = document.createElement('div');
    tooltipElement.className = 'url-tooltip';
    tooltipElement.style.visibility = 'visible';
    tooltipElement.style.opacity = '1';
    tooltipElement.textContent = fullUrl;
    
    // Add to body
    document.body.appendChild(tooltipElement);
    
    // Position tooltip
    const rect = tooltipElement.getBoundingClientRect();
    const x = event.clientX;
    const y = event.clientY;
    
    // Position above the cursor, but check if it would go off screen
    let left = x - rect.width / 2;
    let top = y - rect.height - 10;
    
    // Adjust if tooltip would go off the left edge
    if (left < 10) left = 10;
    
    // Adjust if tooltip would go off the right edge
    if (left + rect.width > window.innerWidth - 10) {
        left = window.innerWidth - rect.width - 10;
    }
    
    // Adjust if tooltip would go off the top
    if (top < 10) {
        top = y + 20; // Show below cursor instead
    }
    
    tooltipElement.style.left = left + 'px';
    tooltipElement.style.top = top + 'px';
}

/**
 * Hides the current tooltip
 */
function hideTooltip() {
    if (tooltipElement) {
        tooltipElement.remove();
        tooltipElement = null;
    }
}

/**
 * Shows a tooltip with the full URL at the cursor position
 * @param {Event} event - The mouse event
 * @param {string} fullUrl - The complete URL to display
 */
function showDetailedLogs(result, url) {
    const logContent = `
        <div class="bg-white rounded-lg shadow-xl max-w-2xl mx-auto p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Detailed Test Log</h2>
            <div class="mb-4">
                <h3 class="font-semibold text-gray-800">URL: </h3>
                <div class="text-sm font-mono bg-gray-100 p-2 rounded break-all">${url}</div>
            </div>
            
            <div class="mb-4">
                <h3 class="font-semibold text-gray-800">Final Result:</h3>
                <div class="text-sm">
                    <span class="font-medium">Status:</span> ${result.status}<br>
                    <span class="font-medium">Method:</span> ${result.method}<br>
                    <span class="font-medium">HTTP Status:</span> ${result.http_status}<br>
                    <span class="font-medium">Message:</span> ${result.message}
                </div>
            </div>

            ${result.details && result.details.length > 0 ? `
            <div class="mb-4">
                <h3 class="font-semibold text-gray-800 mb-2">Test Steps:</h3>
                <div class="bg-gray-50 p-3 rounded text-sm font-mono space-y-1">
                    ${result.details.map(detail => `<div>${detail}</div>`).join('')}
                </div>
            </div>
            ` : ''}

            <div class="flex justify-center mt-6">
                <button onclick="this.closest('.fixed').remove()" class="btn-primary">
                    Close
                </button>
            </div>
        </div>
    `;

    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50';
    modal.innerHTML = `
        <div class="relative top-20 mx-auto p-5 border w-11/12 max-w-2xl shadow-lg rounded-md bg-white">
            ${logContent}
        </div>
    `;

    // Close modal when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });    document.body.appendChild(modal);
}

/**
 * Tests any URL manually by opening it in an iframe and monitoring the result
 * @param {string} url - The URL to test manually
 */
function testManualAccess(url) {
        // Get current status to customize the UI
        const currentStatus = getCurrentUrlStatus(url);
        const statusConfig = getStatusConfig(currentStatus);
        
        const modalContent = `
            <div class="bg-white rounded-lg shadow-xl max-w-4xl mx-auto p-6 h-5/6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold text-gray-900">Manual Accessibility Test</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                
                <div class="bg-${statusConfig.color}-50 border-l-4 border-${statusConfig.color}-400 p-4 mb-4">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            ${statusConfig.icon}
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-${statusConfig.color}-700">
                                <strong>Testing URL:</strong> ${url}<br>
                                <strong>Current Status:</strong> ${currentStatus}<br>
                                ${statusConfig.description}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <div class="flex items-center justify-between bg-gray-100 p-3 rounded">
                        <span class="text-sm font-medium text-gray-700">Test Status:</span>
                        <span id="testStatus" class="text-sm font-semibold text-blue-600">Loading...</span>
                    </div>
                </div>

                <div class="border-2 border-gray-300 rounded-lg overflow-hidden" style="height: 60vh;">
                    <iframe id="testFrame" src="${url}" class="w-full h-full" 
                            onload="handleIframeLoad('${url}')" 
                            onerror="handleIframeError('${url}')">
                    </iframe>
                </div>

                <div class="mt-4">
                    <div class="bg-blue-50 p-3 rounded mb-4">
                        <h4 class="font-semibold text-blue-800 mb-2">What to look for:</h4>
                        <ul class="text-sm text-blue-700 space-y-1">
                            <li>• <strong>Full content loading:</strong> Can you see the website's main content?</li>
                            <li>• <strong>Interactive elements:</strong> Do buttons, links, and forms work?</li>
                            <li>• <strong>Media content:</strong> Do images, videos, or embedded content load?</li>
                            <li>• <strong>Error messages:</strong> Are there any "blocked" or "access denied" messages?</li>
                        </ul>
                    </div>
                    
                    <div class="flex justify-between items-center">
                        <div class="text-sm text-gray-600">
                            <strong>Based on what you see above, how would you classify this site's accessibility?</strong>
                        </div>
                        <div class="space-x-2">
                            <button onclick="reportManualResult('${url}', 'fully')" class="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded text-sm">
                                ✓ Fully Works
                            </button>
                            <button onclick="reportManualResult('${url}', 'partial')" class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-2 rounded text-sm">
                                ⚠ Partially Works
                            </button>
                            <button onclick="reportManualResult('${url}', 'blocked')" class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded text-sm">
                                ✗ Blocked/Error
                            </button>
                            <button onclick="window.open('${url}', '_blank')" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded text-sm">
                                Open in New Tab
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50';
        modal.innerHTML = `
            <div class="relative top-10 mx-auto p-5 border w-11/12 max-w-6xl shadow-lg rounded-md bg-white">
                ${modalContent}
            </div>
        `;

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });        document.body.appendChild(modal);

        // Start monitoring the iframe
        setTimeout(() => {
            monitorIframeLoad(url);
        }, 2000);
}

/**
 * Gets the current status of a URL from the table
 * @param {string} url - The URL to find
 * @returns {string} The current status
 */
function getCurrentUrlStatus(url) {
    const tableRows = document.querySelectorAll('tbody tr');
    for (const row of tableRows) {
        const urlCell = row.querySelector('td:first-child');
        if (urlCell && urlCell.textContent.includes(url.split('/')[2])) {
            const statusCell = row.querySelector('td:nth-child(2)');
            return statusCell ? statusCell.textContent.trim() : 'Unknown';
        }
    }
    return 'Unknown';
}

/**
 * Gets configuration for different status types
 * @param {string} status - The current status
 * @returns {Object} Configuration object with color, icon, and description
 */
function getStatusConfig(status) {
    const configs = {
        'Partially Accessible': {
            color: 'yellow',
            icon: `<svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                   </svg>`,
            description: 'Domain is reachable but full content access is uncertain. Let\'s test if the complete page loads properly.'
        },
        'Possibly Reachable': {
            color: 'blue',
            icon: `<svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                   </svg>`,
            description: 'Basic connectivity detected but limited information available. Manual testing will determine actual accessibility.'
        },
        'Not Reachable': {
            color: 'red',
            icon: `<svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                   </svg>`,
            description: 'Automated tests failed to reach this site. Manual testing may reveal if it\'s actually blocked or just having connectivity issues.'
        }
    };
    
    return configs[status] || {
        color: 'gray',
        icon: `<svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
               </svg>`,
        description: 'Status unclear from automated testing. Manual verification will provide definitive results.'
    };
}

/**
 * Monitors iframe loading and updates status
 * @param {string} url - The URL being tested
 */
function monitorIframeLoad(url) {
    const iframe = document.getElementById('testFrame');
    const statusElement = document.getElementById('testStatus');
    
    if (!iframe || !statusElement) return;

    try {
        // Try to access iframe content to see if it loaded successfully
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        
        if (iframeDoc && iframeDoc.readyState === 'complete') {
            // Check if the iframe has actual content
            const bodyContent = iframeDoc.body ? iframeDoc.body.innerHTML : '';
            if (bodyContent.length > 100) { // Arbitrary threshold for "real" content
                statusElement.textContent = 'Loaded Successfully!';
                statusElement.className = 'text-sm font-semibold text-green-600';
                  // Auto-update the result in the table
                setTimeout(() => {
                    const finalStatus = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://') 
                        ? 'Fully Accessible (HTTP Warning)' 
                        : 'Fully Accessible';
                    const finalMessage = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://')
                        ? '⚠️ Site accessible but uses insecure HTTP. Modern browsers may show warnings.'
                        : 'Site fully accessible from school network';
                    updateTableResult(url, finalStatus, 'Manual Test', 'Page loaded in iframe', finalMessage);
                }, 1000);
            } else {
                statusElement.textContent = 'Page appears empty or blocked';
                statusElement.className = 'text-sm font-semibold text-orange-600';
            }
        } else {
            statusElement.textContent = 'Loading or access restricted...';
            statusElement.className = 'text-sm font-semibold text-yellow-600';
        }
    } catch (e) {
        // Cross-origin restriction - iframe loaded but we can't access content
        statusElement.textContent = 'Loaded (cross-origin - likely working)';
        statusElement.className = 'text-sm font-semibold text-blue-600';
          // Assume it's working if we get cross-origin restriction
        setTimeout(() => {
            const finalStatus = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://') 
                ? 'Fully Accessible (HTTP Warning)' 
                : 'Fully Accessible';
            const finalMessage = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://')
                ? '⚠️ Site accessible but uses insecure HTTP. Modern browsers may show warnings.'
                : 'Site accessible but CORS prevents iframe inspection';
            updateTableResult(url, finalStatus, 'Manual Test + CORS', 'Cross-origin access (normal)', finalMessage);
        }, 1000);
    }
}

/**
 * Handles iframe load event
 * @param {string} url - The URL that loaded
 */
function handleIframeLoad(url) {
    const statusElement = document.getElementById('testStatus');
    if (statusElement) {
        statusElement.textContent = 'Frame loaded - checking content...';
        statusElement.className = 'text-sm font-semibold text-blue-600';
    }
    
    // Give it a moment then check the content
    setTimeout(() => monitorIframeLoad(url), 500);
}

/**
 * Handles iframe error event
 * @param {string} url - The URL that failed
 */
function handleIframeError(url) {
    const statusElement = document.getElementById('testStatus');
    if (statusElement) {
        statusElement.textContent = 'Failed to load in iframe';
        statusElement.className = 'text-sm font-semibold text-red-600';
    }
}

/**
 * Reports manual test result and updates the table
 * @param {string} url - The URL tested
 * @param {string} resultType - The result type: 'fully', 'partial', 'blocked'
 */
function reportManualResult(url, resultType) {
    let newStatus, newMethod, newHttpStatus, newMessage, messageText;
      switch (resultType) {
        case 'fully':
            const isHttpOnly = url.toLowerCase().startsWith('http://') && !url.toLowerCase().startsWith('https://');
            newStatus = isHttpOnly ? 'Fully Accessible (HTTP Warning)' : 'Fully Accessible';
            newMethod = 'Manual Confirmation';
            newHttpStatus = 'User Verified';
            newMessage = isHttpOnly 
                ? '⚠️ User confirmed site works but uses insecure HTTP. Modern browsers may show warnings.'
                : 'User confirmed site works completely from school network';
            messageText = `Updated: ${url} marked as ${newStatus} based on manual test`;
            break;
        case 'partial':
            newStatus = 'Partially Accessible';
            newMethod = 'Manual Confirmation';
            newHttpStatus = 'User Verified';
            newMessage = 'User confirmed site partially works (some content may be restricted)';
            messageText = `Updated: ${url} marked as Partially Accessible based on manual test`;
            break;
        case 'blocked':
            newStatus = 'Blocked';
            newMethod = 'Manual Confirmation';
            newHttpStatus = 'User Verified';
            newMessage = 'User confirmed site is blocked or inaccessible from school network';
            messageText = `Updated: ${url} marked as Blocked based on manual test`;
            break;
        default:
            return; // Invalid result type
    }
    
    updateTableResult(url, newStatus, newMethod, newHttpStatus, newMessage);
    displayMessage(messageText, 'info');
    
    // Close the modal
    const modal = document.querySelector('.fixed.inset-0');
    if (modal) modal.remove();
}

/**
 * Updates a result in the table with new status
 * @param {string} url - The URL to update
 * @param {string} newStatus - The new status
 * @param {string} newMethod - The new method
 * @param {string} newHttpStatus - The new HTTP status
 * @param {string} newMessage - The new message
 */
function updateTableResult(url, newStatus, newMethod, newHttpStatus, newMessage) {
    // Find all table rows and update the matching URL
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        const urlCell = row.querySelector('td:first-child');
        if (urlCell && urlCell.textContent.includes(url.split('/')[2])) { // Match by domain
            const cells = row.querySelectorAll('td');
            if (cells.length >= 5) {                // Update status cell with new styling
                const statusCell = cells[1];
                statusCell.textContent = newStatus;
                statusCell.className = `px-6 py-4 text-sm ${getStatusClass(newStatus)}`;
                
                // Update other cells
                cells[2].textContent = newMethod;
                cells[3].textContent = newHttpStatus;
                cells[4].textContent = newMessage;
                  // Update the test button in details cell
                const detailsCell = cells[5];
                if (newStatus.includes('Fully Accessible')) {
                    // Remove the manual test button since it's now confirmed working
                    const testButton = detailsCell.querySelector('button[onclick*="testManualAccess"]');
                    if (testButton) {
                        testButton.remove();
                    }
                } else {                    // Update button text based on new status
                    const testButton = detailsCell.querySelector('button[onclick*="testManualAccess"]');
                    if (testButton) {
                        const buttonText = newStatus.includes('Partially Accessible') ? 'Test Full Access' : 
                                         newStatus.includes('Possibly Reachable') ? 'Verify Access' : 
                                         newStatus === 'Not Reachable' ? 'Retry Test' : 
                                         newStatus === 'Blocked' ? 'Retest' : 'Manual Check';
                        testButton.textContent = buttonText;
                    }
                }
            }
        }
    });
}

// Make functions global so they can be called from HTML
window.showTooltip = showTooltip;
window.hideTooltip = hideTooltip;
window.showDetailedLogs = showDetailedLogs;
window.testManualAccess = testManualAccess;
window.handleIframeLoad = handleIframeLoad;
window.handleIframeError = handleIframeError;
window.reportManualResult = reportManualResult;
window.updateTableResult = updateTableResult;

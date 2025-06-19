document.addEventListener('DOMContentLoaded', () => {
    const csvFile = document.getElementById('csvFile');
    const urlInput = document.getElementById('urlInput');
    const checkButton = document.getElementById('checkButton');
    const loadGoogleSheetButton = document.getElementById('loadGoogleSheetButton');
    const clearButton = document.getElementById('clearButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const reportContainer = document.getElementById('reportContainer');

    // IMPORTANT: Replace this with the actual URL of your Google Sheet published as CSV.
    // How to get this URL:
    // 1. Open your Google Sheet.
    // 2. Go to File > Share > Publish to web.
    // 3. Under the "Link" tab, select the sheet you want to publish.
    // 4. For "Publish as:", choose "Comma-separated values (.csv)".
    // 5. Copy the generated URL. It will look something like:
    //    https://docs.google.com/spreadsheets/d/e/2PACX-1vR-random-string-here/pub?output=csv
    const DEFAULT_GOOGLE_SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/1Zt8Kx8y-placeholder-sheet-id-for-testing-only/pub?output=csv'; // REPLACE ME

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
     */
    function parseTextArea(text) {
        return text.split(/\r?\n/).map(url => url.trim()).filter(url => url !== '');
    }

    /**
     * Checks the reachability of a given URL using a fetch request with 'no-cors' mode.
     * @param {string} url - The URL to check.
     * @param {number} timeout - The maximum number of milliseconds to wait for a response.
     * @returns {Promise<object>} A promise that resolves to an object containing URL check results.
     */
    async function checkUrl(url, timeout = 10000) {
        const result = {
            url: url,
            status: "Error",
            http_status: "N/A",
            message: "An unexpected error occurred."
        };

        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), timeout); // Set timeout

        try {
            // Using 'no-cors' mode is a trade-off. It prevents CORS errors
            // but also makes it impossible to read the actual HTTP status code
            // or response content. If a response is received, it will just be
            // an opaque response. This is good for simply checking reachability
            // without hitting CORS issues, but less informative.
            // For more detailed status (like 404, 500) a server-side proxy
            // or a CORS-enabled endpoint is necessary.
            const response = await fetch(url, {
                method: 'GET',
                mode: 'no-cors', // Crucial for avoiding CORS errors for sites that don't send CORS headers
                signal: controller.signal // Link AbortController to the fetch request
            });
            clearTimeout(id); // Clear the timeout if fetch completes before it fires

            if (response) {
                // With 'no-cors', response.status will always be 0, and response.ok will be true
                // if a network error didn't occur. We can only infer reachability.
                result.status = "Reachable";
                result.http_status = "Opaque Response (due to no-cors)"; // Indicates fetch succeeded but status is unreadable
                result.message = "Successfully initiated fetch. Opaque response (CORS-safe check).";
            } else {
                // This path is less likely with 'no-cors' unless a severe network issue
                result.status = "Not Reachable";
                result.http_status = "N/A";
                result.message = "Network error or no response received.";
            }

        } catch (e) {
            clearTimeout(id); // Clear the timeout on error as well
            result.status = "Not Reachable";
            result.http_status = "N/A";
            if (e.name === 'AbortError') {
                result.message = "Timeout Error: The site took too long to respond.";
            } else if (e instanceof TypeError) {
                // This often indicates a network error (DNS, connection refused)
                // or a CORS blocking issue if 'no-cors' wasn't used.
                result.message = `Network or CORS Error: ${e.message}. Possible network block or server not allowing access.`;
            } else {
                result.message = `An unexpected error occurred: ${e.message}`;
            }
        }
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
            }
            const result = await checkUrl(url);
            results.push(result);
            // Provide real-time feedback (update an existing element or add new for each)
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = 'text-gray-600 text-sm mb-1';
            feedbackDiv.textContent = `[${i + 1}/${urls.length}] Checked: ${url} - Status: ${result.status}`;
            reportContainer.prepend(feedbackDiv); // Add to top for most recent feedback
        }

        loadingIndicator.classList.add('hidden'); // Hide loading indicator

        // Generate summary
        let reachableCount = 0;
        let notReachableCount = 0;
        let errorCount = 0;
        let skippedCount = 0;

        results.forEach(r => {
            if (r.status === "Reachable") reachableCount++;
            else if (r.status === "Not Reachable") notReachableCount++;
            else if (r.status === "Error") errorCount++;
            else if (r.status === "Skipped") skippedCount++;
        });

        const totalUrls = results.length; // Use results.length to account for skipped

        let summaryHtml = `
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Summary of Results</h2>
            <ul class="list-disc list-inside text-gray-700 mb-6">
                <li>Total URLs processed: ${totalUrls}</li>
                <li>Reachable URLs: <span class="text-green-700 font-semibold">${reachableCount}</span></li>
                <li>Not Reachable URLs: <span class="text-red-700 font-semibold">${notReachableCount}</span></li>
                <li>URLs with Errors: <span class="text-orange-700 font-semibold">${errorCount}</span></li>
                <li>Skipped (Empty) URLs: <span class="text-gray-500 font-semibold">${skippedCount}</span></li>
            </ul>
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Detailed Results</h2>
        `;
        // Set innerHTML for summary, then append table
        reportContainer.innerHTML = summaryHtml;

        // Generate detailed table
        if (results.length > 0) {
            const tableHtml = `
                <div class="overflow-x-auto rounded-lg shadow">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tl-lg">URL</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Browser Status/Info</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tr-lg">Message</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            ${results.map(r => `
                                <tr>
                                    <td class="px-6 py-4 whitespace-normal text-sm font-medium text-gray-900">${r.url}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm ${r.status === 'Reachable' ? 'status-reachable' : r.status === 'Not Reachable' ? 'status-not-reachable' : r.status === 'Error' ? 'status-error' : 'status-skipped'}">${r.status}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">${r.http_status}</td>
                                    <td class="px-6 py-4 whitespace-normal text-sm text-gray-500">${r.message}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            reportContainer.innerHTML += tableHtml;
        } else {
            reportContainer.innerHTML += `<p class="text-gray-600">No detailed results to display.</p>`;
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

    // Event listener for the Clear Report button
    clearButton.addEventListener('click', () => {
        reportContainer.innerHTML = '';
        csvFile.value = ''; // Clear file input
        urlInput.value = ''; // Clear textarea
        loadingIndicator.classList.add('hidden');
    });
});

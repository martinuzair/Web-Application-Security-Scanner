# How the Scanner Works (Architecture)

The scanner follows a modular pipeline similar to basic web vulnerability scanning tools.

```text
             ┌──────────────────┐
             │   Target URL     │
             │ http://localhost │
             └─────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Web Crawler   │
              │ discover pages  │
              └─────────┬───────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Form Extractor │
              │ detect inputs   │
              └─────────┬───────┘
                        │
                        ▼
        ┌─────────────────────────────────┐
        │ Vulnerability Scanning Modules  │
        │                                 │
        │ • Security Header Checker       │
        │ • XSS Payload Injection         │
        │ • SQL Injection Probing         │
        └─────────┬───────────────────────┘
                  │
                  ▼
          ┌────────────────────┐
          │   Result Analyzer  │
          │ detect anomalies   │
          └─────────┬──────────┘
                    │
                    ▼
            ┌──────────────────┐
            │ JSON Report File │
            │ reports/report   │
            └──────────────────┘
```

The system is divided into several components:

### 1. Web Crawler

Located in:

```text
crawler.py
```

Responsibilities:

* Discover reachable pages from the target URL
* Stay within the same domain
* Extract HTML forms and input fields

---

### 2. Request Handler

Located in:

```text
utils/request_handler.py
```

Handles:

* HTTP GET requests
* HTTP POST requests
* Request headers
* Error handling and timeouts

Centralizing request logic simplifies vulnerability testing modules.

---

### 3. Vulnerability Modules

Located in:

```text
vulnerabilities/
```

Each vulnerability test is implemented as a separate module.

| Module             | Purpose                              |
| ------------------ | ------------------------------------ |
| `headers.py`       | Detect missing security headers      |
| `xss.py`           | Detect reflected XSS vulnerabilities |
| `sql_injection.py` | Detect possible SQL injection errors |

This modular structure allows new vulnerability checks to be easily added.

Example future modules:

```text
vulnerabilities/
├── directory_discovery.py
├── command_injection.py
├── open_redirect.py
```

---

### 4. Output Formatter

Located in:

```text
utils/output_formatter.py
```

Responsibilities:

* Colored console output
* Formatting scan results
* Saving scan results to JSON reports

---

### 5. Report Generator

Final results are saved in:

```text
reports/report.json
```

This file contains:

* Target scanned
* Pages discovered
* Vulnerabilities detected
* Evidence and payload used

---

# Example Scan Walkthrough

This section demonstrates a basic scan against the intentionally vulnerable application **OWASP Juice Shop**.

---

## Step 1 — Start Juice Shop

Navigate to the Juice Shop directory:

```bash
cd juice-shop
```

Start the application:

```bash
npm start
```

You should see:

```text
Server listening on port 3000
```

Open the application in your browser:

```text
http://localhost:3000
```

---

## Step 2 — Run the Scanner

Open another terminal and run:

```bash
python scanner.py http://localhost:3000
```

---

## Step 3 — Scanner Output

Example console output:

```text
[*] Starting scan on: http://localhost:3000
[*] Max crawl pages: 10
[+] Discovered 1 page(s)

[!] Missing Security Header at http://localhost:3000
    Content-Security-Policy header not found

[!] Missing Security Header at http://localhost:3000
    Strict-Transport-Security header not found

[+] Scan completed
[+] Report saved to reports/report.json
```

---

## Step 4 — Generated Report

Open:

```text
reports/report.json
```

Example:

```json
{
  "target": "http://localhost:3000",
  "pages_discovered": [
    "http://localhost:3000"
  ],
  "findings": [
    {
      "type": "Missing Security Header",
      "url": "http://localhost:3000",
      "evidence": "Content-Security-Policy header not found"
    }
  ]
}
```

---

# Limitations

This scanner is a **learning project**, therefore it has several limitations:

* Limited support for JavaScript-heavy websites
* No authentication handling
* No asynchronous crawling
* Possible false positives

Modern web applications often require more advanced techniques such as:

* headless browser automation
* API endpoint discovery
* JavaScript execution

---

# Future Improvements

Possible enhancements include:

* multi-threaded scanning
* directory brute forcing
* authentication session scanning
* parameter fuzzing
* HTML vulnerability reports
* severity scoring (CVSS style)
* API endpoint discovery
* JavaScript-aware crawling

---

# Disclaimer

This tool is for **educational and research purposes only**.

Do not scan systems without **explicit authorization**.

Use safe targets such as:

* OWASP Juice Shop
* DVWA
* WebGoat

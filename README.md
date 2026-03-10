# Web Application Security Scanner

A simple Python-based web application vulnerability scanner that crawls a website, detects forms, checks missing security headers, and performs basic XSS and SQL injection testing.

This project is intended for **learning and cybersecurity experimentation only**. It should only be used against **authorized targets or intentionally vulnerable applications**.

---

# Features

* Website crawling
* Form detection
* Security header checks
* Basic reflected XSS testing
* Basic SQL injection error detection
* JSON vulnerability reporting

---

# Project Structure

```text
web-vuln-scanner/
│
├── scanner.py
├── crawler.py
├── requirements.txt
│
├── vulnerabilities/
│   ├── __init__.py
│   ├── headers.py
│   ├── sql_injection.py
│   └── xss.py
│
├── utils/
│   ├── __init__.py
│   ├── request_handler.py
│   └── output_formatter.py
│
├── reports/
│   └── report.json
│
└── juice-shop/
    ├── package.json
    ├── server.js
    ├── config/
    ├── frontend/
    ├── routes/
    └── ...
```

The **`juice-shop` directory** contains the intentionally vulnerable web application used as a testing target for the scanner.

---

# Requirements

* Python 3.10+
* Node.js 18+
* npm
* Git

---

# Installing Dependencies

Navigate to the scanner project folder:

```bash
cd web-vuln-scanner
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

# Running OWASP Juice Shop (Test Target)

Navigate into the Juice Shop directory:

```bash
cd juice-shop
```

Install Node dependencies:

```bash
npm install
```

Start the vulnerable web application:

```bash
npm start
```

Juice Shop will start running at:

```text
http://localhost:3000
```

Leave this terminal running while performing scans.

---

# Running the Web Vulnerability Scanner

Open another terminal window and navigate back to the scanner root folder:

```bash
cd web-vuln-scanner
```

Activate the virtual environment if necessary.

Run the scanner against Juice Shop:

```bash
python scanner.py http://localhost:3000
```

Optional crawl limit:

```bash
python scanner.py http://localhost:3000 --max-pages 10
```

---

# Scan Report

After the scan completes, results are saved in:

```text
reports/report.json
```

Example output:

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

# Legal Notice

This project is intended for **educational purposes only**.

Only scan applications where you have **explicit authorization**.

Recommended safe targets include:

* OWASP Juice Shop
* DVWA (Damn Vulnerable Web Application)
* WebGoat

---

# Future Improvements

Possible enhancements include:

* multi-threaded crawling
* directory brute forcing
* authentication support
* parameter fuzzing
* HTML/PDF vulnerability reports
* vulnerability severity scoring

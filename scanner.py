import argparse
from crawler import WebCrawler
from vulnerabilities.headers import check_headers
from vulnerabilities.xss import test_xss_on_form
from vulnerabilities.sql_injection import test_sqli_on_form
from utils.output_formatter import info, success, warning, error, save_report


def main():
    parser = argparse.ArgumentParser(description="Simple Web Application Security Scanner")
    parser.add_argument("url", help="Target URL to scan, e.g. http://localhost:3000")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum pages to crawl")
    args = parser.parse_args()

    target_url = args.url
    max_pages = args.max_pages

    info(f"Starting scan on: {target_url}")
    info(f"Max crawl pages: {max_pages}")

    crawler = WebCrawler(target_url, max_pages=max_pages)
    urls = crawler.crawl()

    if not urls:
        error("No URLs discovered. Exiting.")
        return

    success(f"Discovered {len(urls)} page(s).")

    report = {
        "target": target_url,
        "pages_discovered": urls,
        "findings": []
    }

    for url in urls:
        info(f"Checking page: {url}")

        # Header checks
        header_findings = check_headers(url)
        for finding in header_findings:
            warning(f"{finding['type']} at {finding['url']} - {finding['evidence']}")
            report["findings"].append(finding)

        # Form extraction
        forms = crawler.extract_forms(url)
        if forms:
            info(f"Found {len(forms)} form(s) on {url}")

        # XSS checks
        for form in forms:
            xss_findings = test_xss_on_form(form)
            for finding in xss_findings:
                warning(f"{finding['type']} at {finding['url']} - {finding['evidence']}")
                report["findings"].append(finding)

        # SQLi checks
        for form in forms:
            sqli_findings = test_sqli_on_form(form)
            for finding in sqli_findings:
                warning(f"{finding['type']} at {finding['url']} - {finding['evidence']}")
                report["findings"].append(finding)

    success("Scan completed.")

    if not report["findings"]:
        info("No obvious findings detected by the current checks.")
    else:
        success(f"Total findings: {len(report['findings'])}")

    save_report(report)


if __name__ == "__main__":
    main()
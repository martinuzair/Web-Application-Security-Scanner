from utils.request_handler import get

IMPORTANT_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "Referrer-Policy"
]


def check_headers(url):
    findings = []

    response = get(url)
    if not response:
        return findings

    headers = response.headers

    for header in IMPORTANT_HEADERS:
        if header not in headers:
            findings.append({
                "type": "Missing Security Header",
                "url": url,
                "evidence": f"{header} header not found"
            })

    return findings
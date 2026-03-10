from utils.request_handler import get, post

SQLI_PAYLOADS = [
    "'",
    "\"",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "'--",
]

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "postgresql",
    "ora-01756",
    "syntax error"
]


def test_sqli_on_form(form_details):
    findings = []

    target_url = form_details["action"]
    method = form_details["method"]
    inputs = form_details["inputs"]

    for payload in SQLI_PAYLOADS:
        data = {}

        for field in inputs:
            name = field.get("name")
            field_type = field.get("type", "text")

            if not name:
                continue

            if field_type in ["text", "search", "email", "password", "textarea", "url"]:
                data[name] = payload
            else:
                data[name] = "test"

        if not data:
            continue

        if method == "post":
            response = post(target_url, data=data)
        else:
            response = get(target_url, params=data)

        if response:
            body_lower = response.text.lower()
            for error_string in SQL_ERRORS:
                if error_string in body_lower:
                    findings.append({
                        "type": "Possible SQL Injection",
                        "url": target_url,
                        "payload": payload,
                        "evidence": f"Detected SQL error message: {error_string}"
                    })
                    return findings

    return findings
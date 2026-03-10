from utils.request_handler import get, post

XSS_PAYLOAD = "<script>alert('xss')</script>"


def test_xss_on_form(form_details):
    findings = []

    target_url = form_details["action"]
    method = form_details["method"]
    inputs = form_details["inputs"]

    data = {}

    for field in inputs:
        name = field.get("name")
        field_type = field.get("type", "text")

        if not name:
            continue

        if field_type in ["text", "search", "email", "textarea", "url", "password"]:
            data[name] = XSS_PAYLOAD
        else:
            data[name] = "test"

    if not data:
        return findings

    if method == "post":
        response = post(target_url, data=data)
    else:
        response = get(target_url, params=data)

    if response and XSS_PAYLOAD in response.text:
        findings.append({
            "type": "Possible Reflected XSS",
            "url": target_url,
            "payload": XSS_PAYLOAD,
            "evidence": "Payload reflected in response"
        })

    return findings
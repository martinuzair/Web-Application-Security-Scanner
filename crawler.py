from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from utils.request_handler import get


class WebCrawler:
    def __init__(self, base_url, max_pages=20):
        self.base_url = base_url.rstrip("/")
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = [self.base_url]
        self.domain = urlparse(self.base_url).netloc

    def is_same_domain(self, url):
        return urlparse(url).netloc == self.domain

    def normalize_url(self, current_url, link):
        return urljoin(current_url, link).split("#")[0]

    def crawl(self):
        discovered = []

        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)

            if url in self.visited:
                continue

            response = get(url)
            if not response or "text/html" not in response.headers.get("Content-Type", ""):
                self.visited.add(url)
                continue

            self.visited.add(url)
            discovered.append(url)

            soup = BeautifulSoup(response.text, "html.parser")

            for anchor in soup.find_all("a", href=True):
                new_url = self.normalize_url(url, anchor["href"])

                if self.is_same_domain(new_url) and new_url not in self.visited and new_url not in self.to_visit:
                    self.to_visit.append(new_url)

        return discovered

    def extract_forms(self, url):
        response = get(url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        form_details = []

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()

            inputs = []
            for input_tag in form.find_all(["input", "textarea", "select"]):
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name")
                inputs.append({
                    "type": input_type,
                    "name": input_name
                })

            form_details.append({
                "action": urljoin(url, action) if action else url,
                "method": method,
                "inputs": inputs
            })

        return form_details
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analyze_onpage(url: str) -> dict:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        meta_desc = md.get("content").strip()

    h_tags = {f"h{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")] for i in range(1, 7)}
    imgs = [{"src": urljoin(url, img.get("src", "")), "alt": img.get("alt", "")} for img in soup.find_all("img")]
    links = [{"href": urljoin(url, a.get("href", "")), "text": a.get_text(strip=True)} for a in soup.find_all("a") if a.get("href")]

    # text content for keyword analysis
    for s in soup(["script", "style", "noscript"]):
        s.extract()
    text_content = soup.get_text(separator=" ").strip()

    return {
        "title": title,
        "meta_description": meta_desc,
        "headings": h_tags,
        "images": imgs[:100],
        "links": links[:200],
        "text_content": text_content[:200000],
    }

#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_base_url(config_path):
    text = read_text(config_path)
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("baseURL:"):
            _, value = line.split(":", 1)
            value = value.strip().strip('"').strip("'")
            if value:
                return value
    return ""


def detect_key(static_dir):
    if not os.path.isdir(static_dir):
        return ""
    for name in os.listdir(static_dir):
        m = re.fullmatch(r"([0-9a-f]{32})\.txt", name)
        if m:
            return m.group(1)
    return ""


def validate_key(static_dir, key):
    if not key:
        return False
    path = os.path.join(static_dir, f"{key}.txt")
    if not os.path.isfile(path):
        return False
    content = read_text(path).strip()
    return content == key


def read_sitemap(sitemap_path):
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0].strip("{")
    loc_tag = f"{{{ns}}}loc" if ns else "loc"
    urls = []
    for loc in root.findall(f".//{loc_tag}"):
        if loc.text:
            urls.append(loc.text.strip())
    return urls


def post_indexnow(api_url, payload, dry_run=False):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"HTTP {resp.status}")
            if body:
                print(body)
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}")
        if body:
            print(body)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow.")
    parser.add_argument("--config", default="config.yaml", help="Path to Hugo config.")
    parser.add_argument("--static", dest="static_dir", default="static", help="Static dir.")
    parser.add_argument("--sitemap", default="public/sitemap.xml", help="Path to sitemap.xml.")
    parser.add_argument("--key", default="", help="IndexNow key.")
    parser.add_argument("--key-location", default="", help="Full key file URL.")
    parser.add_argument("--host", default="", help="Host, e.g. codealan.top.")
    parser.add_argument("--url", action="append", default=[], help="Submit a single URL (repeatable).")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending.")
    args = parser.parse_args()

    base_url = load_base_url(args.config)
    if not base_url:
        print("Missing baseURL in config.")
        return 1

    key = args.key or detect_key(args.static_dir)
    if not key:
        print("Missing key. Provide --key or add key file under static/.")
        return 1

    if not validate_key(args.static_dir, key):
        print("Key file missing or content mismatch under static/.")
        return 1

    parsed = urllib.parse.urlparse(base_url)
    host = args.host or parsed.netloc
    if not host:
        print("Missing host. Provide --host or fix baseURL.")
        return 1

    key_location = args.key_location or urllib.parse.urljoin(base_url.rstrip("/") + "/", f"{key}.txt")

    if args.url:
        url_list = args.url
    else:
        if not os.path.isfile(args.sitemap):
            print("Missing sitemap.xml. Run ./build.sh first or pass --url.")
            return 1
        url_list = read_sitemap(args.sitemap)

    if not url_list:
        print("No URLs to submit.")
        return 1

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list,
    }
    return post_indexnow("https://api.indexnow.org/IndexNow", payload, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

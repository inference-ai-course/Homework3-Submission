"""
Web Scraping Utilities -- Week 3

Functions for extracting clean text from web pages using
trafilatura (traditional) and Crawl4AI (modern LLM-ready).

Functions:
  extract_with_trafilatura(url)    - Extract text using trafilatura
  extract_with_crawl4ai(url)       - Extract LLM-ready markdown with Crawl4AI
  scrape_arxiv_abstracts(topic, n) - Scrape arXiv paper abstracts
  compare_extractors(url)          - Side-by-side comparison of both tools
"""

import os
import json
from typing import Dict, List, Optional, Any


def extract_with_trafilatura(url: str, include_tables: bool = False) -> Dict[str, Any]:
    """
    Extract clean text from a URL using trafilatura.

    Args:
        url: Web page URL
        include_tables: Whether to include table content

    Returns:
        Dict with 'text', 'url', 'method', 'char_count' keys
    """
    try:
        import trafilatura
    except ImportError:
        raise ImportError("Install: pip install trafilatura")

    import requests
    import time

    print(f"[trafilatura] Fetching: {url}")
    start = time.time()

    response = requests.get(url, timeout=15, headers={
        'User-Agent': 'Mozilla/5.0 (research-bot)'
    })
    html = response.text

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=include_tables,
    )

    elapsed = time.time() - start

    result = {
        "text": text or "",
        "url": url,
        "method": "trafilatura",
        "char_count": len(text) if text else 0,
        "elapsed_seconds": round(elapsed, 2),
    }

    print(f"  Extracted {result['char_count']:,} chars in {elapsed:.1f}s")
    return result


def extract_with_crawl4ai(url: str) -> Dict[str, Any]:
    """
    Extract LLM-ready markdown from a URL using Crawl4AI.

    Crawl4AI produces clean markdown optimized for LLM consumption,
    automatically removing navigation, ads, and boilerplate.

    NOTE: Crawl4AI requires Python 3.10+. If unavailable, falls back
    to html2text for markdown conversion.

    Args:
        url: Web page URL

    Returns:
        Dict with 'text', 'url', 'method', 'char_count' keys
    """
    import sys
    import time

    # Try Crawl4AI first (requires Python 3.10+)
    if sys.version_info >= (3, 10):
        try:
            from crawl4ai import AsyncWebCrawler
            import asyncio

            print(f"[Crawl4AI] Fetching: {url}")
            start = time.time()

            async def _crawl():
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url)
                    return result.markdown if result.success else ""

            async def _crawl():
                async with AsyncWebCrawler() as crawler:
                    result = await crawler.arun(url=url)
                    return result.markdown if result.success else ""

            def _run_in_new_thread():
                """
                Spawn a brand-new ProactorEventLoop in a worker thread.
                This sidesteps any existing SelectorEventLoop in the main thread
                (common in Jupyter and Windows Store Python).
                """
                if sys.platform == "win32":
                    loop = asyncio.ProactorEventLoop()   # ← explicit, not just policy
                else:
                    loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(_crawl())
                finally:
                    loop.close()

            import concurrent.futures

            try:
                asyncio.get_running_loop()
                # ── Already inside a running loop (Jupyter / async context) ──
                # Can't call asyncio.run() here, so delegate to a thread
                # that owns its own fresh ProactorEventLoop.
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    text = pool.submit(_run_in_new_thread).result()
            except RuntimeError:
                # ── No running loop (plain .py script) ──
                text = _run_in_new_thread()

            elapsed = time.time() - start
            result = {
                "text": text or "",
                "url": url,
                "method": "crawl4ai",
                "char_count": len(text) if text else 0,
                "elapsed_seconds": round(elapsed, 2),
            }
            print(f"  Extracted {result['char_count']:,} chars in {elapsed:.1f}s")
            return result

        except ImportError:
            print("  [Crawl4AI not installed -- falling back to html2text]")

    # Fallback: requests + html2text for markdown conversion
    return _extract_as_markdown(url)


def _extract_as_markdown(url: str) -> Dict[str, Any]:
    """
    Fallback markdown extractor using html2text (works on Python 3.9+).

    Converts HTML to clean Markdown, preserving links and structure --
    similar to what Crawl4AI does but without browser rendering.
    """
    import time

    try:
        import html2text
    except ImportError:
        raise ImportError("Install: pip install html2text")

    import requests as req

    print(f"[html2text] Fetching: {url}")
    start = time.time()

    resp = req.get(url, timeout=15, headers={
        'User-Agent': 'Mozilla/5.0 (research-bot)'
    })

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.skip_internal_links = True

    text = h.handle(resp.text).strip()

    elapsed = time.time() - start

    result = {
        "text": text,
        "url": url,
        "method": "html2text (markdown fallback)",
        "char_count": len(text),
        "elapsed_seconds": round(elapsed, 2),
    }

    print(f"  Extracted {result['char_count']:,} chars in {elapsed:.1f}s")
    return result


def scrape_arxiv_abstracts(
    topic: str = "large language models",
    max_results: int = 5,
    save_path: Optional[str] = None,
) -> List[Dict[str, str]]:
    import requests
    import xml.etree.ElementTree as ET
    import time

    print("=" * 55)
    print(f"Scraping arXiv: '{topic}' (max {max_results} papers)")
    print("=" * 55)

    base_url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    # Retry logic: try up to 3 times
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"  Attempt {attempt}/{max_retries}...")
            response = requests.get(base_url, params=params, timeout=60)

            # Handle rate limiting specifically
            if response.status_code == 429:
                wait = 30 * attempt  # wait 30s, 60s, 90s
                print(f"  Rate limited (429). Waiting {wait}s before retry...")
                time.sleep(wait)
                continue  # go back to top of loop

            response.raise_for_status()
            break  # success

        except requests.Timeout:
            print(f"  Timeout on attempt {attempt}. ", end="")
            if attempt < max_retries:
                wait = attempt * 5
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("All attempts failed.")
                return []

        except requests.RequestException as e:
            print(f"  Request error: {e}")
            return []

    if not response.text.strip():
        print("Warning: Empty response from arXiv API")
        return []

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        print(f"Raw response (first 300 chars): {response.text[:300]}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        abstract = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
        url = entry.find("atom:id", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]

        papers.append({
            "title": title,
            "abstract": abstract,
            "url": url,
            "authors": authors,
        })

        print(f"\n  [{len(papers)}] {title[:80]}...")
        print(f"      Authors: {', '.join(authors[:3])}{'...' if len(authors) > 3 else ''}")
        print(f"      Abstract: {abstract[:120]}...")
        time.sleep(0.5)

    print(f"\n  Total papers collected: {len(papers)}")

    if save_path:
        os.makedirs(os.path.dirname(save_path) or '.', exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        print(f"  Saved to: {save_path}")

    return papers


def compare_extractors(url: str) -> Dict[str, Any]:
    """
    Side-by-side comparison of trafilatura vs Crawl4AI on the same URL.

    Args:
        url: Web page URL to test

    Returns:
        Dict with results from both extractors and comparison metrics
    """
    print("=" * 55)
    print("EXTRACTOR COMPARISON")
    print("=" * 55)
    print(f"URL: {url}\n")

    traf_result = extract_with_trafilatura(url)

    try:
        c4ai_result = extract_with_crawl4ai(url)
    except ImportError:
        print("  [Crawl4AI not installed -- skipping]")
        c4ai_result = {"text": "", "char_count": 0, "elapsed_seconds": 0, "method": "crawl4ai (not installed)"}

    c4ai_label = c4ai_result.get('method', 'crawl4ai')
    print(f"\n--- Comparison ---")
    print(f"  trafilatura:  {traf_result['char_count']:,} chars in {traf_result['elapsed_seconds']:.1f}s")
    print(f"  {c4ai_label}: {c4ai_result['char_count']:,} chars in {c4ai_result['elapsed_seconds']:.1f}s")

    return {
        "url": url,
        "trafilatura": traf_result,
        "crawl4ai": c4ai_result,
    }

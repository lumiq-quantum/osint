"""
marc-osint-server
=================
MCP server exposing public information searches: news, obituaries, and
public social media signal checks.

Status: news_search and obituary_search are REAL (Google News RSS).
social_signal_check remains mocked pending DPDP sign-off per §13.6.
"""
from typing import Any
import os
import httpx
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "marc-osint-server",
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8004")),
)


def _google_news_rss(query: str, max_results: int = 10) -> list[dict]:
    """Fetch results from Google News RSS feed."""
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        resp = httpx.get(url, timeout=15, follow_redirects=True)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.text)
        items = root.findall(".//item")
        results = []
        for item in items[:max_results]:
            title = item.find("title")
            link = item.find("link")
            pub_date = item.find("pubDate")
            source = item.find("source")
            results.append({
                "title": title.text if title is not None else "",
                "source": source.text if source is not None else "",
                "url": link.text if link is not None else "",
                "date": pub_date.text if pub_date is not None else "",
            })
        return results
    except Exception:
        return []


@mcp.tool()
def news_search(name: str, location: str, date_range: str) -> dict[str, Any]:
    """Search Google News for public mentions of the deceased. §13.5. REAL."""
    query = f"{name} {location} {date_range}"
    results = _google_news_rss(query, max_results=10)
    return {
        "query": query,
        "result_count": len(results),
        "results": results,
        "mocked": False,
    }


@mcp.tool()
def obituary_search(name: str, location: str) -> dict[str, Any]:
    """Search Google News for published obituaries. §13.5. REAL."""
    query = f"{name} obituary {location}"
    results = _google_news_rss(query, max_results=5)
    return {
        "query": query,
        "result_count": len(results),
        "results": results,
        "mocked": False,
    }


@mcp.tool()
def social_signal_check(name: str, location: str, dob: str) -> dict[str, Any]:
    """Public social media signal check. §13.6.
    DPDP-compliant: only public profiles, full audit log. MOCK."""
    return {
        "platforms_queried": ["facebook", "instagram", "linkedin", "x"],
        "profiles_examined": [],
        "signals": [],
        "verdict": "no-signal",
        "dpdp_audit_id": "DPDP-MOCK-001",
        "mocked": True,
    }


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run()

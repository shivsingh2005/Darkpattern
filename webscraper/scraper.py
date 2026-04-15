import asyncio
import importlib
import re
from typing import Any

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
BLOCKED_TITLE_TERMS = [
    "Robot",
    "CAPTCHA",
    "Access Denied",
    "403",
    "Blocked",
    "Attention Required",
]


class ScraperBlockedError(Exception):
    pass


class ScraperTimeoutError(Exception):
    pass


URGENCY_REGEX = re.compile(
  r"(\b\d+\s*(left|remaining|in stock|available)\b|\bonly\s+\d+\b|\bjust\s+\d+\b|\blast\s+\d+\b)",
  re.IGNORECASE,
)
TIMER_REGEX = re.compile(
  r"(\b\d{1,2}:\d{2}(:\d{2})?\b|\b\d+\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)\b|\b(ends?|expires?)\s+in\b|\bcount\s?down\b|\btimer\b)",
  re.IGNORECASE,
)
SOCIAL_REGEX = re.compile(
  r"(\b\d+\s*(people|users|customers|others|viewing|bought|purchased|watching)\b|bestseller|most popular|top rated|#1|\b\d+(\.\d+)?\s*stars?\b|\b\d+\s*reviews?\b)",
  re.IGNORECASE,
)
CHECKOUT_REGEX = re.compile(
  r"(shipping|delivery|fee|charge|tax|total|convenience fee|handling|\$|£|€)",
  re.IGNORECASE,
)
CTA_REGEX = re.compile(
  r"(no thanks|no, i|i don't want|i prefer not|skip|decline|i hate|i'd rather|i'll pass|without|subscribe|cancel|free trial|add to cart|buy now|checkout|continue|agree)",
  re.IGNORECASE,
)


def _clean_full_text(raw_text: str) -> str:
    deduped_lines: list[str] = []
    seen: set[str] = set()

    for line in str(raw_text).splitlines():
        cleaned = " ".join(line.split()).strip()
        if len(cleaned) < 8:
            continue
        if re.fullmatch(r"[\d\W_]+", cleaned):
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        deduped_lines.append(cleaned)

    return "\n".join(deduped_lines)


def _extract_priority_elements(lines: list[str]) -> dict[str, list[str]]:
    urgency: list[str] = []
    timers: list[str] = []
    popups: list[str] = []
    cta_buttons: list[str] = []
    checkout: list[str] = []
    social_proof: list[str] = []

    for line in lines:
        if URGENCY_REGEX.search(line):
            urgency.append(line)
        if TIMER_REGEX.search(line):
            timers.append(line)
        if SOCIAL_REGEX.search(line):
            social_proof.append(line)
        if CHECKOUT_REGEX.search(line):
            checkout.append(line)
        if CTA_REGEX.search(line):
            cta_buttons.append(line)

        lowered = line.lower()
        if any(term in lowered for term in ("cookie", "newsletter", "overlay", "popup", "subscribe")):
            popups.append(line)

    def unique(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    return {
        "urgency_scarcity": unique(urgency),
        "timer_countdown": unique(timers),
        "popups_overlays": unique(popups),
        "cta_buttons": unique(cta_buttons),
        "checkout_price_text": unique(checkout),
        "social_proof": unique(social_proof),
    }


def _scrape_structured_fallback(url: str) -> dict[str, Any]:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en-IN,en;q=0.9"},
            timeout=20,
        )
        response.raise_for_status()
    except requests.Timeout as exc:
        raise ScraperTimeoutError("Timed out while loading the page.") from exc
    except requests.RequestException as exc:
        raise ScraperBlockedError(f"Could not fetch URL content: {exc}") from exc

    soup = BeautifulSoup(response.text, "lxml")
    page_title = (soup.title.string or "").strip() if soup.title else ""
    full_text = _clean_full_text(soup.get_text("\n", strip=True))
    lines = full_text.splitlines()

    if any(term.lower() in page_title.lower() for term in BLOCKED_TITLE_TERMS):
        raise ScraperBlockedError("This site is blocking automated access. Try again later.")

    return {
        "url": url,
        "page_title": page_title,
        "full_text": full_text,
        "priority_elements": _extract_priority_elements(lines),
    }


async def _scrape_structured_async(url: str) -> dict[str, Any]:
    playwright_async = importlib.import_module("playwright.async_api")
    playwright_stealth = importlib.import_module("playwright_stealth")

    PlaywrightError = getattr(playwright_async, "Error")
    PlaywrightTimeoutError = getattr(playwright_async, "TimeoutError")
    async_playwright = getattr(playwright_async, "async_playwright")
    stealth_async = getattr(playwright_stealth, "stealth_async")

    async def _handle_route(route) -> None:
        if route.request.resource_type in {"image", "font", "media"}:
            await route.abort()
            return
        await route.continue_()

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1366, "height": 768},
                locale="en-IN",
                timezone_id="Asia/Kolkata",
                extra_http_headers={
                    "Accept-Language": "en-IN,en;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
            )

            await context.route("**/*", _handle_route)

            page = await context.new_page()
            await stealth_async(page)

            await page.goto(url, wait_until="networkidle", timeout=45000)
            await page.wait_for_timeout(2000)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            title = (await page.title()) or ""
            body_text = await page.evaluate("document.body ? document.body.innerText : ''")
            if any(term.lower() in title.lower() for term in BLOCKED_TITLE_TERMS):
                raise ScraperBlockedError("This site is blocking automated access. Try again later.")

            extracted = await page.evaluate(
                r"""
                () => {
                  const visibleText = (el) => {
                    if (!el) return "";
                    const style = window.getComputedStyle(el);
                    if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) {
                      return "";
                    }
                    return (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim();
                  };

                  const pushIf = (arr, value) => {
                    if (value && value.length > 0) arr.push(value);
                  };

                  const unique = (arr) => [...new Set(arr.filter(Boolean).map((item) => item.trim()).filter((item) => item.length > 0))];

                  const urgency = [];
                  const timers = [];
                  const popups = [];
                  const ctaButtons = [];
                  const checkout = [];
                  const socialProof = [];

                  const urgencyRegex = /(\b\d+\s*(left|remaining|in stock|available)\b|\bonly\s+\d+\b|\bjust\s+\d+\b|\blast\s+\d+\b)/i;
                  const timerRegex = /(\b\d{1,2}:\d{2}(:\d{2})?\b|\b\d+\s*(h|hr|hrs|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)\b|\b(ends?|expires?)\s+in\b|\bcount\s?down\b|\btimer\b)/i;
                  const socialRegex = /(\b\d+\s*(people|users|customers|others|viewing|bought|purchased|watching)\b|bestseller|most popular|top rated|#1|\b\d+(\.\d+)?\s*stars?\b|\b\d+\s*reviews?\b)/i;
                  const checkoutRegex = /(shipping|delivery|fee|charge|tax|total|convenience fee|handling|₹|\$|£|€)/i;
                  const ctaRegex = /(no thanks|no, i|i don't want|i prefer not|skip|decline|i hate|i'd rather|i'll pass|without|subscribe|cancel|free trial|add to cart|buy now|checkout|continue|agree)/i;

                  document.querySelectorAll("*").forEach((el) => {
                    const text = visibleText(el);
                    if (!text) return;

                    const idClass = `${el.id || ""} ${(el.className || "").toString()}`.toLowerCase();

                    if (urgencyRegex.test(text) || /(stock|scarcity|remaining|inventory|left|timer|countdown|clock|counter)/i.test(idClass)) {
                      pushIf(urgency, text);
                    }

                    if (timerRegex.test(text) || /(timer|countdown|clock|counter)/i.test(idClass)) {
                      pushIf(timers, text);
                    }

                    if (socialRegex.test(text)) {
                      pushIf(socialProof, text);
                    }

                    if (checkoutRegex.test(text)) {
                      pushIf(checkout, text);
                    }
                  });

                  document.querySelectorAll("button, a").forEach((el) => {
                    const text = visibleText(el);
                    if (ctaRegex.test(text)) {
                      pushIf(ctaButtons, text);
                    }

                    if (checkoutRegex.test(text)) {
                      pushIf(checkout, text);
                    }

                    const parentText = visibleText(el.parentElement);
                    if (checkoutRegex.test(parentText)) {
                      pushIf(checkout, parentText);
                    }
                  });

                  document.querySelectorAll("*").forEach((el) => {
                    const role = (el.getAttribute("role") || "").toLowerCase();
                    const style = window.getComputedStyle(el);
                    const idClass = `${el.id || ""} ${(el.className || "").toString()}`.toLowerCase();
                    const text = visibleText(el);
                    if (!text) return;

                    const isDialog = role === "dialog" || role === "alertdialog";
                    const isOverlay = /(modal|popup|overlay|banner|cookie|newsletter|offer)/i.test(idClass);
                    const isFloating = style.position === "fixed" || style.position === "absolute";

                    if ((isDialog || isOverlay || isFloating) && style.display !== "none") {
                      pushIf(popups, text);
                    }
                  });

                  return {
                    page_title: document.title || "",
                    full_text: document.body ? document.body.innerText : "",
                    priority_elements: {
                      urgency_scarcity: unique(urgency),
                      timer_countdown: unique(timers),
                      popups_overlays: unique(popups),
                      cta_buttons: unique(ctaButtons),
                      checkout_price_text: unique(checkout),
                      social_proof: unique(socialProof),
                    },
                  };
                }
                """
            )

            await context.close()
            await browser.close()

            cleaned_full_text = _clean_full_text(extracted.get("full_text", ""))
            return {
                "url": url,
                "page_title": extracted.get("page_title", title),
                "full_text": cleaned_full_text,
                "priority_elements": extracted.get("priority_elements", {}),
            }
    except Exception as exc:
        if isinstance(exc, PlaywrightTimeoutError):
            raise ScraperTimeoutError("Timed out while loading the page.") from exc
        if isinstance(exc, ScraperBlockedError):
            raise
        if isinstance(exc, PlaywrightError):
            raise ScraperBlockedError("This site is blocking automated access. Try again later.") from exc
        raise


def scrape_structured(url: str) -> dict[str, Any]:
  try:
    return asyncio.run(_scrape_structured_async(url))
  except ScraperBlockedError as exc:
    message = str(exc).lower()
    if "executable" in message or "browser" in message:
      return _scrape_structured_fallback(url)
    raise
  except (ImportError, ModuleNotFoundError, NotImplementedError):
    return _scrape_structured_fallback(url)
  except RuntimeError as exc:
    # Some Windows/Python builds can raise runtime errors while creating subprocesses.
    if "subprocess" in str(exc).lower() or "event loop" in str(exc).lower():
      return _scrape_structured_fallback(url)
    return _scrape_structured_fallback(url)


def get_text_content(url: str) -> str:
    return scrape_structured(url).get("full_text", "")


def scrape_url(url: str) -> dict[str, Any]:
    structured = scrape_structured(url)
    return {
        "url": structured.get("url", url),
        "success": True,
        "text_content": structured.get("full_text", ""),
        "links": [],
        "images": [],
        "error": None,
    }


class WebScraper:
    def __init__(self, timeout: int = 45):
        self.timeout = timeout

    def get_text_content(self, url: str) -> str:
        return get_text_content(url)

    def scrape(self, url: str) -> dict[str, Any]:
        return scrape_url(url)

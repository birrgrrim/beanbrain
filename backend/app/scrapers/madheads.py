import re

import httpx

from ..schemas import ScrapeResult
from .base import BaseScraper

# MadHeads property IDs from their SvelteKit data
PROPERTY_IDS = {
    16: "country",
    32: "flavor_profile",
    39: "processing",
    35: "sweetness",
    34: "acidity",
    33: "bitterness",
    29: "score",
    27: "roast_type",
    36: "variety",
    13: "roaster_comment",
    14: "roaster_comment",
}

CDN_BASE = "https://api.madheadscoffee.com/cdn"


def _unescape_js(s: str) -> str:
    """Unescape JS unicode sequences like \\u002F -> /"""
    return re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda m: chr(int(m.group(1), 16)),
        s,
    )


class MadHeadsScraper(BaseScraper):
    @staticmethod
    def can_handle(url: str) -> bool:
        return "madheadscoffee.com" in url

    @staticmethod
    def _normalize_url(url: str) -> tuple[str, str]:
        """Return (canonical_url, en_url) from any MadHeads product URL."""
        # Extract slug from URL patterns like:
        # /p/FSSwZVjt58s or /en/p/FSSwZVjt58s
        match = re.search(r"/p/([^/?#]+)", url)
        if not match:
            raise ValueError(f"Cannot extract product slug from URL: {url}")
        slug = match.group(1)
        base = "https://madheadscoffee.com"
        return f"{base}/p/{slug}", f"{base}/en/p/{slug}"

    @staticmethod
    def _extract_data(html: str) -> dict:
        """Extract the SvelteKit embedded data from HTML."""
        match = re.search(r"const data = (\[.*?\]);\n", html, re.DOTALL)
        if not match:
            raise ValueError("Could not find SvelteKit data in page")

        raw = match.group(1)

        # Extract product block using regex
        product = {}

        # Product label (name)
        label_match = re.search(r'product:\{id:(\d+)[^}]*?label:"([^"]*)"', raw)
        if label_match:
            product["id"] = int(label_match.group(1))
            product["label"] = label_match.group(2)

        # i18n labels
        product["i18n"] = {}
        for m in re.finditer(
            r'\{lang:"(en|uk)",product_id:\d+,label:"([^"]*)",'
            r'description_short:"([^"]*)"',
            raw,
        ):
            product["i18n"][m.group(1)] = {
                "label": m.group(2),
                "description_short": m.group(3),
            }

        # Product image
        photo_match = re.search(r'photos:\[\{ext:"(\w+)",path:"([^"]+)"\}', raw)
        if photo_match:
            product["image_path"] = _unescape_js(photo_match.group(2))
            product["image_ext"] = photo_match.group(1)

        # Characteristics
        product["characteristics"] = {}

        # Find all characteristic option blocks with property info
        # Pattern: property_id:N ... i18n:[{lang:"en"...label:"X"},{lang:"uk"...label:"Y"}]
        char_pattern = re.compile(
            r'property_id:(\d+),label:"([^"]*)".*?'
            r'i18n:\[\{lang:"en",option_id:\d+,label:"([^"]*)"\},'
            r'\{lang:"uk",option_id:\d+,label:"([^"]*)"\}\]',
            re.DOTALL,
        )

        for m in char_pattern.finditer(raw):
            prop_id = int(m.group(1))
            prop_name = PROPERTY_IDS.get(prop_id)
            if not prop_name:
                continue

            en_val = _unescape_js(m.group(3))
            uk_val = _unescape_js(m.group(4))

            if prop_name == "flavor_profile":
                product["characteristics"].setdefault("flavor_profile", {"en": [], "uk": []})
                product["characteristics"]["flavor_profile"]["en"].append(en_val)
                product["characteristics"]["flavor_profile"]["uk"].append(uk_val)
            else:
                product["characteristics"][prop_name] = {"en": en_val, "uk": uk_val}

        # Prices — product-level price + first variant's retail/wholesale
        price_match = re.search(r'price:(\d+)', raw)
        if price_match:
            product["price"] = int(price_match.group(1))
        wholesale_match = re.search(r'price_wholesale:(\d+)', raw)
        if wholesale_match:
            product["price_wholesale"] = int(wholesale_match.group(1))

        return product

    async def scrape(self, url: str) -> ScrapeResult:
        uk_url, en_url = self._normalize_url(url)

        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(en_url)
            resp.raise_for_status()

        data = self._extract_data(resp.text)
        chars = data.get("characteristics", {})

        # Build image URL
        image_url = None
        if data.get("image_path"):
            image_url = f"{CDN_BASE}{data['image_path']}large.{data.get('image_ext', 'png')}"

        # Determine roast level from roast_type characteristic
        roast = chars.get("roast_type", {}).get("en")

        # Parse score as int
        score = None
        score_str = chars.get("score", {}).get("en", "")
        if score_str:
            try:
                score = int(score_str.split("/")[0])
            except (ValueError, IndexError):
                pass

        def _parse_metric(val: str | None) -> int | None:
            if not val:
                return None
            try:
                return int(val.split("/")[0])
            except (ValueError, IndexError):
                return None

        return ScrapeResult(
            name=data.get("label", ""),
            roastery="MadHeads",
            price=data.get("price"),
            price_wholesale=data.get("price_wholesale"),
            origin=chars.get("country", {}).get("en"),
            process=chars.get("processing", {}).get("en"),
            roast_level=roast,
            roastery_url=uk_url,
            image_url=image_url,
            score=score,
            sweetness=_parse_metric(chars.get("sweetness", {}).get("en")),
            acidity=_parse_metric(chars.get("acidity", {}).get("en")),
            bitterness=_parse_metric(chars.get("bitterness", {}).get("en")),
            flavor_descriptors=chars.get("flavor_profile", {}),
            name_i18n={
                lang: info["label"]
                for lang, info in data.get("i18n", {}).items()
                if isinstance(info, dict) and "label" in info
            },
            roaster_comment=chars.get("roaster_comment", {}),
        )

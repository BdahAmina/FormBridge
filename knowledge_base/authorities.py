"""Allowlisted official authorities and seed URLs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Authority:
    key: str
    name_he: str
    name_en: str
    source_type: str  # official | secondary
    priority: int
    allowed_domains: tuple[str, ...]
    seed_urls: tuple[str, ...]
    categories: tuple[str, ...]
    form_hints: tuple[str, ...]
    enabled: bool = True
    fixture_file: str = ""


AUTHORITIES: dict[str, Authority] = {
    "btl": Authority(
        key="btl",
        name_he="המוסד לביטוח לאומי",
        name_en="National Insurance Institute",
        source_type="official",
        priority=1,
        allowed_domains=("www.btl.gov.il", "btl.gov.il"),
        seed_urls=("https://www.btl.gov.il/",),
        categories=("אבטלה", "נכות", "לידה", "קצבאות", "תביעות"),
        form_hints=("1500", "ביטוח לאומי", "דמי אבטלה", "אבטלה", "נכות", "לידה"),
        fixture_file="btl.html",
    ),
    "govil": Authority(
        key="govil",
        name_he="GOV.IL",
        name_en="GOV.IL",
        source_type="official",
        priority=2,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he",),
        categories=("שירותים ממשלתיים", "טפסים"),
        form_hints=("gov.il", "ממשלה", "שירות ממשלתי", "portal", "government services"),
        fixture_file="govil.html",
    ),
    "tax": Authority(
        key="tax",
        name_he="רשות המסים",
        name_en="Israel Tax Authority",
        source_type="official",
        priority=1,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he/departments/israel_tax_authority",),
        categories=("מס הכנסה", "תיאום מס", "החזר"),
        form_hints=("101", "טופס 101", "רשות המסים", "מס הכנסה", "תיאום מס"),
        fixture_file="tax.html",
    ),
    "piba": Authority(
        key="piba",
        name_he="רשות האוכלוסין וההגירה",
        name_en="Population and Immigration Authority",
        source_type="official",
        priority=1,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he/departments/population_and_immigration_authority",),
        categories=("תעודת זהות", "דרכון", "כתובת", "ויזה"),
        form_hints=("אוכלוסין", "דרכון", "תעודת זהות", "שינוי כתובת", "ויזה"),
        fixture_file="piba.html",
    ),
    "labor": Authority(
        key="labor",
        name_he="משרד העבודה",
        name_en="Ministry of Labor",
        source_type="official",
        priority=1,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he/departments/ministry_of_labor",),
        categories=("עבודה", "פיטורים", "חופשה"),
        form_hints=("משרד העבודה", "פיטורים", "זכויות עובדים", "חופשה"),
        fixture_file="labor.html",
    ),
    "health": Authority(
        key="health",
        name_he="משרד הבריאות",
        name_en="Ministry of Health",
        source_type="official",
        priority=1,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he/departments/ministry_of_health",),
        categories=("בריאות", "זכויות רפואיות"),
        form_hints=("משרד הבריאות", "קופת חולים", "בריאות"),
        fixture_file="health.html",
    ),
    "education": Authority(
        key="education",
        name_he="משרד החינוך",
        name_en="Ministry of Education",
        source_type="official",
        priority=1,
        allowed_domains=("www.gov.il", "gov.il"),
        seed_urls=("https://www.gov.il/he/departments/ministry_of_education",),
        categories=("רישום", "מלגות", "חינוך מיוחד"),
        form_hints=("משרד החינוך", "רישום לבית ספר", "מלגה"),
        fixture_file="education.html",
    ),
    "kolzchut": Authority(
        key="kolzchut",
        name_he="כל זכות",
        name_en="Kol Zchut",
        source_type="secondary",
        priority=4,
        allowed_domains=("www.kolzchut.org.il", "kolzchut.org.il"),
        seed_urls=("https://www.kolzchut.org.il/",),
        categories=("הסבר משני", "זכויות"),
        form_hints=("כל זכות", "kolzchut"),
        fixture_file="kolzchut.html",
    ),
}


def get_authority(key: str) -> Authority | None:
    return AUTHORITIES.get(key)


def official_authorities() -> list[Authority]:
    return [item for item in AUTHORITIES.values() if item.enabled]


def is_allowed_url(url: str) -> bool:
    lowered = url.lower()
    for authority in AUTHORITIES.values():
        if any(domain in lowered for domain in authority.allowed_domains):
            if lowered.startswith("https://"):
                return True
    return False


def source_priority(authority_key: str) -> int:
    authority = AUTHORITIES.get(authority_key)
    return authority.priority if authority else 99

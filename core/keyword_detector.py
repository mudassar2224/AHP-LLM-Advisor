"""
keyword_detector.py
────────────────────
Scans any user prompt, matches against the keyword→capability map,
and returns a normalized capability-weight vector.
This vector drives the AHP domain-fit score.
"""

import csv
from collections import defaultdict


# ─────────────────────────────────────────────
# Loader
# ─────────────────────────────────────────────
def load_keyword_map(csv_path: str) -> dict:
    """
    Returns  { keyword: { cap_name: weight, ... }, ... }
    """
    kmap = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kw   = row["keyword"].strip().lower()
            caps = {}
            for pair in row["capability_weights"].split(","):
                pair = pair.strip()
                if ":" not in pair:
                    continue
                cap, w = pair.split(":", 1)
                caps[cap.strip()] = float(w.strip())
            if caps:
                kmap[kw] = caps
    return kmap


# ─────────────────────────────────────────────
# Detection
# ─────────────────────────────────────────────
def detect_keywords(prompt: str, keyword_map: dict) -> list[tuple[str, dict]]:
    """
    Returns a list of (keyword, cap_weights) for every keyword found in prompt.
    Sorted longest-match first to prefer specific matches.
    """
    prompt_lower = prompt.lower()
    found = []
    for kw, caps in keyword_map.items():
        if kw in prompt_lower:
            found.append((kw, caps))
    # Longer keywords first (more specific)
    found.sort(key=lambda x: -len(x[0]))
    return found


# ─────────────────────────────────────────────
# Weight merger
# ─────────────────────────────────────────────
def merge_cap_weights(detected: list[tuple[str, dict]]) -> dict:
    """
    Combines capability weights from all matched keywords
    and normalizes to sum = 1.0
    """
    if not detected:
        return {}

    merged = defaultdict(float)
    for _, caps in detected:
        for cap, w in caps.items():
            merged[cap] += w

    total = sum(merged.values())
    if total == 0:
        return {}

    return {cap: round(w / total, 4) for cap, w in merged.items()}


# ─────────────────────────────────────────────
# Domain classifier
# ─────────────────────────────────────────────
# Domains checked first — most specific / technical win over generic
_PRIORITY_DOMAINS = ["rag", "cybersecurity", "multilingual", "healthcare", "legal", "banking"]

def classify_domain(prompt: str, domain_keywords: dict) -> str:
    """
    Returns the most likely domain name string, or 'default'.
    Priority domains are checked first so 'rag chatbot' → rag, not chatbot.
    """
    prompt_lower = prompt.lower()

    # 1) High-priority / specific domains — first match wins
    for domain in _PRIORITY_DOMAINS:
        if domain not in domain_keywords:
            continue
        for kw in domain_keywords[domain]:
            if kw in prompt_lower:
                return domain

    # 2) General scoring for the rest
    scores = defaultdict(int)
    for domain, kws in domain_keywords.items():
        if domain in _PRIORITY_DOMAINS:
            continue
        for kw in kws:
            if kw in prompt_lower:
                scores[domain] += 1

    if not scores:
        return "default"
    return max(scores, key=scores.get)

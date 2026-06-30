"""
ahp_engine.py  —  AHP scoring engine (fixed cost normalization + coding weights)
"""

import math
import pandas as pd
from core.keyword_detector import detect_keywords, merge_cap_weights, classify_domain
import config


# ─────────────────────────────────────────────
# LOG-SCALE COST NORMALIZATION
# ─────────────────────────────────────────────
def log_cost_score(cost_in: float, cost_out: float) -> float:
    """
    Log-normalized cost score so premium models (Claude, GPT) are not
    crushed vs cheap models (Gemini Flash, Llama).

    Linear scale (old): Claude cost=0.10,  Gemini=0.80  ← too extreme
    Log scale    (new): Claude cost=0.13,  Gemini=0.41  ← proportional

    Range: 0.05 (most expensive) → 0.96 (cheapest)
    """
    total_usd_per_m = (cost_in + cost_out) * 1000   # convert to $/M tokens
    if total_usd_per_m <= 0:
        return 1.0
    # Anchor: cheapest known ~$0.15/M (Phi-4 Mini), priciest ~$180/M (GPT-5.5 High)
    score = 1.0 - math.log10(1 + total_usd_per_m) / math.log10(181)
    return round(max(0.0, min(1.0, score)), 4)


# ─────────────────────────────────────────────
# AHP PAIRWISE NORMALIZATION
# ─────────────────────────────────────────────
def normalize_pairwise(matrix: list) -> tuple:
    n = len(matrix)
    col_sums = [sum(matrix[r][c] for r in range(n)) for c in range(n)]
    norm     = [[matrix[r][c] / col_sums[c] for c in range(n)] for r in range(n)]
    weights  = [sum(norm[r][c] for c in range(n)) / n for r in range(n)]

    lam_max = sum(
        sum(matrix[r][c] * weights[c] for c in range(n)) / weights[r]
        for r in range(n)
    ) / n
    ci = (lam_max - n) / (n - 1) if n > 1 else 0
    ri = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12}
    cr = ci / ri.get(n, 1.12)
    return weights, round(cr, 4)


# ─────────────────────────────────────────────
# DOMAIN → AHP CRITERION WEIGHTS
# Criteria order: [Performance, Cost, Safety, DomainFit]
# ─────────────────────────────────────────────
def get_ahp_weights(domain: str) -> tuple:
    matrices = {
        # CODING — performance dominates; cost is secondary
        # Real devs pick the best coder, not the cheapest
        "coding": [
            [1,    7,   5,   9],   # Perf is 7x > Cost, 5x > Safety
            [1/7,  1,   1,   3],
            [1/5,  1,   1,   3],
            [1/9, 1/3, 1/3,  1],
        ],
        # BANKING / HEALTHCARE / LEGAL — safety first
        "banking": [
            [1,   3,  1/3,  5],
            [1/3, 1,  1/7,  3],
            [3,   7,  1,    7],
            [1/5, 1/3,1/7,  1],
        ],
        "healthcare": [
            [1,   3,  1/3,  5],
            [1/3, 1,  1/7,  3],
            [3,   7,  1,    7],
            [1/5, 1/3,1/7,  1],
        ],
        "legal": [
            [1,   2,  1/3,  5],
            [1/2, 1,  1/5,  3],
            [3,   5,  1,    7],
            [1/5, 1/3,1/7,  1],
        ],
        # CREATIVE — performance + domain fit balanced
        "creative": [
            [1,   1,   5,   1/2],
            [1,   1,   5,   1/2],
            [1/5, 1/5, 1,   1/5],
            [2,   2,   5,   1  ],
        ],
        # VIDEO — domain fit (multimodal) is most critical
        "video": [
            [1,   1,   5,   1/3],
            [1,   1,   5,   1/3],
            [1/5, 1/5, 1,   1/5],
            [3,   3,   5,   1  ],
        ],
        # RAG — performance + long context dominate; cheap models can't do RAG well
        # Perf ≈ 65%, Cost ≈ 13%, Safety ≈ 12%, DomainFit ≈ 10%
        "rag": [
            [1,   5,   5,   7],   # Perf >> Cost (RAG needs quality reasoning)
            [1/5, 1,   1,   2],
            [1/5, 1,   1,   2],
            [1/7, 1/2, 1/2, 1],
        ],
        # EDUCATION — balanced performance + cost
        "education": [
            [1,   1,   3,   3],
            [1,   1,   3,   3],
            [1/3, 1/3, 1,   2],
            [1/3, 1/3, 1/2, 1],
        ],
        # ECOMMERCE — performance dominates (coding + content quality)
        # Perf≈62%, Cost≈18%, Safety≈12%, DomFit≈8%
        "ecommerce": [
            [1,   4,   5,   7],
            [1/4, 1,   2,   3],
            [1/5, 1/2, 1,   2],
            [1/7, 1/3, 1/2, 1],
        ],
        # CYBERSECURITY — performance + safety
        "cybersecurity": [
            [1,   3,   1,   7],
            [1/3, 1,   1/3, 3],
            [1,   3,   1,   7],
            [1/7, 1/3, 1/7, 1],
        ],
        # CHATBOT — performance > cost (good chat quality matters)
        # Perf≈52%, Cost≈28%, Safety≈10%, DomFit≈10%
        "chatbot": [
            [1,   2,   5,   5],
            [1/2, 1,   3,   3],
            [1/5, 1/3, 1,   1],
            [1/5, 1/3, 1,   1],
        ],
        # RESEARCH — performance + safety
        "research": [
            [1,   2,   2,   3],
            [1/2, 1,   1,   2],
            [1/2, 1,   1,   2],
            [1/3, 1/2, 1/2, 1],
        ],
        # MULTILINGUAL — domain fit (multilingual cap) is key
        "multilingual": [
            [1,   1,   2,   1/2],
            [1,   1,   2,   1/2],
            [1/2, 1/2, 1,   1/3],
            [2,   2,   3,   1  ],
        ],
        # DEFAULT — performance leads (unknown task = quality over cheapness)
        # Perf≈56%, Cost≈22%, Safety≈14%, DomFit≈8%
        "default": [
            [1,   3,   4,   7],
            [1/3, 1,   2,   3],
            [1/4, 1/2, 1,   2],
            [1/7, 1/3, 1/2, 1],
        ],
    }
    mat = matrices.get(domain, matrices["default"])
    return normalize_pairwise(mat)


# ─────────────────────────────────────────────
# MAIN AHP SCORING FUNCTION
# ─────────────────────────────────────────────
def compute_ahp_scores(
    prompt:      str,
    dataset:     pd.DataFrame,
    keyword_map: dict,
    top_k:       int = 5,
) -> tuple:
    """
    Returns: (top_models, cap_weights, ahp_weights, domain, cr)
    """
    # 1 — detect keywords + capability weights
    detected    = detect_keywords(prompt, keyword_map)
    cap_weights = merge_cap_weights(detected)

    # 2 — classify domain
    domain = classify_domain(prompt, config.DOMAIN_KEYWORDS)

    # 3 — AHP criterion weights for this domain
    ahp_weights, cr = get_ahp_weights(domain)

    # 4 — fallback cap weights if nothing detected
    if not cap_weights:
        cap_weights = {
            "chat":                   0.30,
            "reasoning":              0.30,
            "instruction_following":  0.25,
            "factual_accuracy":       0.15,
        }

    # 5 — score every model using LOG-SCALE cost
    results = []
    for _, row in dataset.iterrows():
        # Domain fit = weighted capability match
        domain_fit = sum(
            float(row.get(f"cap_{cap}", 0)) * w
            for cap, w in cap_weights.items()
        )

        perf   = float(row.get("performance_composite", 0))
        safety = float(row.get("safety_composite", 0))

        # ★ Use log-scale cost instead of pre-computed linear cost_composite
        cost = log_cost_score(
            float(row.get("cost_per_1k_input_usd",  0.01)),
            float(row.get("cost_per_1k_output_usd", 0.03)),
        )

        ahp_score = (
            ahp_weights[0] * perf       +
            ahp_weights[1] * cost       +
            ahp_weights[2] * safety     +
            ahp_weights[3] * domain_fit
        )

        results.append({
            "model_name":    row.get("model_name", ""),
            "company":       row.get("company", ""),
            "country":       row.get("country", ""),
            "license":       row.get("license", ""),
            "open_source":   int(row.get("open_source", 0)),
            "ahp_score":     round(ahp_score, 4),
            "performance":   round(perf, 4),
            "cost_score":    round(cost, 4),
            "safety":        round(safety, 4),
            "domain_fit":    round(domain_fit, 4),
            "cost_in":       float(row.get("cost_per_1k_input_usd", 0)),
            "cost_out":      float(row.get("cost_per_1k_output_usd", 0)),
            "latency_ms":    int(row.get("latency_ms", 0)),
            "context_k":     int(row.get("context_window_k", 128)),
            "free_tier":     int(row.get("free_tier", 0)),
            "self_hostable": int(row.get("self_hostable", 0)),
            "arena_overall": float(row.get("arena_overall_score", 0)),
            "hallucination": float(row.get("hallucination_rate", 0)),
            "cap_coding":    float(row.get("cap_coding", 0)),
            "cap_reasoning": float(row.get("cap_reasoning", 0)),
            "cap_multimodal_image": float(row.get("cap_multimodal_image", 0)),
            "cap_multimodal_video": float(row.get("cap_multimodal_video", 0)),
            "cap_multilingual":     float(row.get("cap_multilingual", 0)),
        })

    results.sort(key=lambda x: -x["ahp_score"])
    return results[:top_k], cap_weights, ahp_weights, domain, cr

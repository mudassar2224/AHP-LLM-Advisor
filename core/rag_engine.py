"""
rag_engine.py
─────────────
Loads the LLM master dataset and builds structured RAG context
for the Groq LLM to use when answering user prompts.
"""

import pandas as pd


# ─────────────────────────────────────────────
# Dataset loader
# ─────────────────────────────────────────────
def load_dataset(csv_path: str) -> pd.DataFrame:
    """Loads and validates the master LLM dataset."""
    df = pd.read_csv(csv_path)
    # Ensure numeric columns are float
    numeric_cols = [
        "performance_composite", "cost_composite_score", "safety_composite",
        "cost_per_1k_input_usd", "cost_per_1k_output_usd",
        "latency_ms", "context_window_k", "hallucination_rate",
        "arena_overall_score",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


# ─────────────────────────────────────────────
# Context formatter for Groq
# ─────────────────────────────────────────────
def format_context(
    top_models:  list[dict],
    prompt:      str,
    cap_weights: dict,
    ahp_weights: list[float],
    domain:      str,
    cr:          float,
) -> str:
    """
    Builds a rich context string that Groq uses to give
    accurate, data-driven recommendations.
    """
    w = ahp_weights  # [Perf, Cost, Safety, DomainFit]

    lines = [
        f'═══ AHP ANALYSIS FOR: "{prompt}" ═══',
        f"Detected Domain       : {domain.upper()}",
        f"Consistency Ratio     : {cr:.4f} {'✓ Valid' if cr < 0.10 else '⚠ Check'}",
        "",
        "AHP CRITERION WEIGHTS (how much each factor matters):",
        f"  Performance   {w[0]:.1%}",
        f"  Cost          {w[1]:.1%}",
        f"  Safety/Trust  {w[2]:.1%}",
        f"  Domain Fit    {w[3]:.1%}",
        "",
        f"KEY CAPABILITIES DETECTED: {', '.join(cap_weights.keys())}",
        "",
        f"TOP {len(top_models)} RECOMMENDED MODELS (by AHP score):",
        "─" * 50,
    ]

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, m in enumerate(top_models):
        medal = medals[i] if i < len(medals) else f"#{i+1}"
        cost_str = f"${m['cost_in']:.4f}/1k in  •  ${m['cost_out']:.4f}/1k out"
        oss_str  = "✅ Open Source" if m["open_source"] else "🔒 Proprietary"
        free_str = "🆓 Free tier"  if m["free_tier"]   else ""
        host_str = "💻 Self-hostable" if m["self_hostable"] else ""

        lines += [
            f"",
            f"{medal} {m['model_name']}  ({m['company']}, {m['country']})",
            f"   AHP Score     : {m['ahp_score']:.4f}",
            f"   Performance   : {m['performance']:.1%}   |  Domain Fit : {m['domain_fit']:.1%}",
            f"   Safety        : {m['safety']:.1%}   |  Cost Score : {m['cost_score']:.1%}",
            f"   Pricing       : {cost_str}",
            f"   Latency       : {m['latency_ms']} ms  |  Context : {m['context_k']}K tokens",
            f"   Arena Score   : {m['arena_overall']:.1f}/100  |  Hallucination : {m['hallucination']:.1%}",
            f"   License       : {m['license']}  {oss_str}  {free_str}  {host_str}",
        ]

    lines += ["", "═" * 50]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# Quick stats helper (used by sidebar)
# ─────────────────────────────────────────────
def get_dataset_stats(dataset: pd.DataFrame) -> dict:
    return {
        "total_models": len(dataset),
        "companies":    dataset["company"].nunique(),
        "open_source":  int(dataset["open_source"].sum()),
        "free_tier":    int(dataset["free_tier"].sum()),
        "avg_score":    round(dataset["performance_composite"].mean() * 100, 1),
    }

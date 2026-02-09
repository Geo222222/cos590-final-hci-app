import numpy as np

def recommendation_from_score(score: float):
    """
    Fixed recommendation logic (controlled variable for your study).
    """
    if score < 0.33:
        return "LOW", "Maintain allocation", "Risk appears manageable given current metrics."
    elif score < 0.66:
        return "MEDIUM", "Rebalance toward diversification", "Moderate risk; consider reducing concentration and downside exposure."
    else:
        return "HIGH", "Reduce exposure / increase safety buffer", "High risk; consider de-risking or hedging to reduce downside."

def explanation_text(hhi, semidev, mdd, var, es, score):
    parts = []
    if hhi >= 0.45:
        parts.append("• Concentration is high (HHI suggests the portfolio is dominated by few holdings).")
    elif hhi >= 0.33:
        parts.append("• Concentration is moderate (HHI indicates meaningful exposure to a few holdings).")
    else:
        parts.append("• Diversification is relatively strong (HHI indicates weights are distributed).")

    if semidev >= 0.02:
        parts.append("• Downside volatility is elevated (semideviation below 0% is high).")
    elif semidev >= 0.01:
        parts.append("• Downside volatility is moderate (some negative-return variability).")
    else:
        parts.append("• Downside volatility is low (limited negative-return variability).")

    if mdd <= -0.20:
        parts.append("• Max drawdown is large (recent peak-to-trough decline is significant).")
    elif mdd <= -0.10:
        parts.append("• Max drawdown is moderate (notable decline from peak).")
    else:
        parts.append("• Max drawdown is small (portfolio has not declined sharply from peak).")

    if (not np.isnan(var)) and var <= -0.03:
        parts.append("• Tail risk is elevated (VaR suggests relatively large potential losses in worst periods).")
    if (not np.isnan(es)) and es <= -0.03:
        parts.append("• Expected shortfall indicates heavy losses in the worst tail events.")

    parts.append(f"• Combined risk score: {score:.2f} (fixed rule-based blend for controlled evaluation).")
    return "\n".join(parts)

def counterfactual_suggestion(hhi, semidev, mdd, var, es, score):
    suggestions = []
    if hhi > 0.40:
        suggestions.append("If the largest positions were reduced and weights spread more evenly, concentration risk (HHI) would drop.")
    if semidev > 0.015:
        suggestions.append("If downside volatility decreased (e.g., shifting to lower-vol assets), semideviation would drop.")
    if mdd < -0.15:
        suggestions.append("If drawdowns were reduced (smaller peak-to-trough declines), the drawdown component would improve.")
    if (not np.isnan(var)) and var < -0.02:
        suggestions.append("If worst-period losses improved, VaR/ES would be less negative (lower tail risk).")
    if not suggestions:
        suggestions.append("Risk is already in a lower range; only major market shifts would materially change the recommendation.")
    return " ".join(suggestions)
0 
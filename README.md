# COS590 / HCI Application Development Prototype
## AI-Assisted Investment Decision-Support System (Portfolio Risk + Transparency Study)

A working Streamlit prototype aligned to the COS590 final paper concept: an AI-assisted investment
decision-support interface focused on portfolio risk assessment and explanation transparency
(human-in-the-loop). This is **not** an automated trading system.

The app generates recommendations, supports confidence/trust logging, and includes two interface
conditions for HCI evaluation:

- `EXPLANATION_OFF` → Recommendation-only UI
- `EXPLANATION_ON` → Recommendation + Explanation + optional Counterfactual UI

---

## What The Application Does

### Decision Support (Portfolio Level)
Given a user-defined portfolio allocation (weights), the system:

1. Simulates return behavior (for demo + repeatability)
2. Computes interpretable risk metrics (HHI, Semideviation, Max Drawdown, VaR, ES)
3. Produces a fixed rule-based risk score (0–1) and a recommendation (LOW, MEDIUM, HIGH)

Recommendation mapping:
- LOW → Maintain allocation
- MEDIUM → Rebalance toward diversification
- HIGH → Reduce exposure / increase safety buffer

### HCI Evaluation Mode
The app supports evaluation data capture:

- Decision: Accept / Reject / Unsure
- Confidence (1–7) and Trust (1–7)
- Optional SUS (System Usability Scale) survey (0–100)
- Export of all logs to CSV/JSON

This is designed so you can write a Results section with:

- Task completion outcomes
- Acceptance rates across conditions
- Trust calibration signals
- SUS score summary

---

## Why This Is Research-Aligned
Modern Human-AI Interaction and Explainable AI research emphasizes:

- Human-in-the-loop decision support
- Transparency and explanations (progressive disclosure)
- Trust calibration and appropriate reliance
- Controlled interface condition comparisons

This prototype implements those principles directly through:

- `EXPLANATION_ON` vs `EXPLANATION_OFF` conditions
- Logging user decisions + trust/confidence
- Explanation + optional counterfactual statements
- Traceable, interpretable metrics (not black-box outputs)

---

## Repository Structure

- `app.py`
- `requirements.txt`
- `README.md`

---

## Installation

### Requirements
- Python 3.9+ recommended

### Setup (macOS/Linux)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Reproducibility And Environment

- Dependencies are listed in `requirements.txt`.
- Record `python --version` and `streamlit --version` in your report.
- Returns are simulated for repeatability and offline execution.

---

## Run The Application
```bash
streamlit run app.py
```

Streamlit will open the UI in your browser.

---

## How To Use (Quick Guide)

### Step 1 — Set The Study Condition
In the sidebar, choose:
- `EXPLANATION_OFF` (recommendation-only)
- `EXPLANATION_ON` (recommendation + explanation)

### Step 2 — Configure A Portfolio
- Set number of assets
- Adjust allocation weights
- Set VaR/ES alpha (tail probability)
- Optional toggles: Counterfactual explanation; Loss-aversion framing

### Step 3 — Review The Outputs
Dashboard outputs:
- Risk level + risk score
- Equity curve and return distribution
- Risk metric table
- Recommendation

Explainability outputs:
- Equations (HHI, VaR, ES, portfolio return)
- Traceability table
- Controlled recommendation logic snippet

### Step 4 — Log Evaluation Data
Submit:
- Decision (Accept/Reject/Unsure)
- Confidence (1–7)
- Trust (1–7)

Optionally submit:
- SUS survey (0–100)

### Step 5 — Export Logs
Go to Evaluation & Export:
- Download `logs.csv`
- Download `logs.json`

---

## Metrics And Equations Used

### Concentration (HHI)
HHI measures how concentrated the portfolio is. Higher HHI = fewer holdings dominate risk.

Plain-text:
HHI = Σ(w_i^2)

LaTeX:
$$
HHI = \sum_{i=1}^{N} w_i^2
$$

### Portfolio Return

Plain-text:
r_p(t) = Σ(w_i * r_i(t))

LaTeX:
$$
r_p(t) = \sum_{i=1}^{N} w_i\, r_i(t)
$$

### Tail Risk (VaR / ES)

Plain-text:
VaR_α = Q_α(r_p)
ES_α = E[r_p | r_p ≤ VaR_α]

LaTeX:
$$
VaR_\alpha = Q_\alpha(r_p)
$$

$$
ES_\alpha = E\left[ r_p \mid r_p \le VaR_\alpha \right]
$$

---

## Controlled Recommendation Logic

The recommendation engine is intentionally fixed rule-based logic so the experiment isolates UI
explanation effects, not model variance.

- `score < 0.33` → LOW → Maintain
- `0.33 ≤ score < 0.66` → MEDIUM → Rebalance
- `score ≥ 0.66` → HIGH → Reduce exposure

---

## Evaluation Design (Recommended For Your Paper)

Suggested mini-study:
- 3–5 participants (minimum viable)

Tasks:
- Interpret recommendation and risk level
- Adjust allocation to reduce risk
- Compare trust/confidence between conditions

Report:
- Acceptance rate by condition
- Average trust/confidence by condition
- SUS mean score
- Qualitative notes (confusion points)

---

## Data, Privacy, And Ethics Notes

- The prototype uses simulated returns by default for repeatability and offline execution.
- Evaluation logs are generated locally and exported by the user.
- Do not collect unnecessary personal data beyond a participant ID.

---

## Notes / Limitations

- Return data is simulated for repeatability and offline execution.
- Risk scoring is a simplified blend for HCI controlled testing.
- This prototype is intended for HCI evaluation, not production investing.

---

## Cite This Project

If you reference this prototype, use a short course-project style citation like:

```bibtex
@misc{cos590_hci_app,
  title        = {AI-Assisted Investment Decision-Support System (Portfolio Risk + Transparency Study)},
  author       = {YOUR NAME},
  year         = {YEAR},
  howpublished = {Course project, COS590},
  note         = {Streamlit prototype for HCI evaluation}
}
```

---

## References (2018+)

- Amershi, S., Weld, D., Vorvoreanu, M., Fourney, A., Nushi, B., Collisson, P., Suh, J., Iqbal, S., Bennett, P. N., Inkpen, K., Teevan, J., Kikin-Gil, R., Horvitz, E. (2019). Guidelines for Human-AI Interaction. CHI 2019. DOI: 10.1145/3290605.3300233.
- Leichtmann, B., Humer, C., Hinterreiter, A., Streit, M., Mara, M. (2023). Effects of Explainable Artificial Intelligence on trust and human behavior in a high-risk decision task. Computers in Human Behavior, 139, 107539. DOI: 10.1016/j.chb.2022.107539.
- Kim, J., Maathuis, H., Sent, D. (2024). Human-centered evaluation of explainable AI applications: a systematic review. Frontiers in Artificial Intelligence, 7. DOI: 10.3389/frai.2024.1456486.
- Tabassi, E. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1. DOI: 10.6028/NIST.AI.100-1.

---

## License

Academic prototype — add a license if needed (MIT recommended).

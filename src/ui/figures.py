from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import streamlit as st


def _ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def render_architecture_figure(export_dir: str = "artifacts", filename_prefix: str = "fig_"):
    """
    Renders a simple, IEEE-friendly system architecture figure and optionally exports it to disk.
    This is a pragmatic “figure generator” for your paper submission.
    """
    st.subheader("System Architecture Figure (Exportable)")

    filename = f"{filename_prefix}system_architecture.png"
    export_path = _ensure_dir(export_dir) / filename

    fig = plt.figure(figsize=(12, 3.2))
    ax = plt.gca()
    ax.axis("off")

    # Box layout coordinates
    boxes = [
        ("User Inputs\n(Weights, Alpha,\nCondition)", 0.02, 0.25, 0.18, 0.5),
        ("Market Data\n(Real ETH/USDT\n+ Synthetic)", 0.23, 0.25, 0.18, 0.5),
        ("Risk Metrics\n(HHI, SemiDev,\nMDD, VaR, ES)", 0.44, 0.25, 0.18, 0.5),
        ("Controlled Scoring\n+ Recommendation\n(LOW/MED/HIGH)", 0.65, 0.25, 0.18, 0.5),
        ("UI Condition\n(EXPL_OFF/ON)\n+ Explanations", 0.86, 0.25, 0.12, 0.5),
    ]

    # Draw rectangles
    for label, x, y, w, h in boxes:
        rect = plt.Rectangle((x, y), w, h, fill=False, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9)

    # Arrows
    def arrow(x1, y1, x2, y2):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", linewidth=1.5),
        )

    arrow(0.20, 0.50, 0.23, 0.50)
    arrow(0.41, 0.50, 0.44, 0.50)
    arrow(0.62, 0.50, 0.65, 0.50)
    arrow(0.83, 0.50, 0.86, 0.50)

    # Logging path
    ax.text(0.86, 0.08, "Evaluation Logging\n(Decision, Trust,\nConfidence, SUS)\n→ CSV/JSON Export",
            ha="center", va="center", fontsize=9)
    arrow(0.92, 0.25, 0.92, 0.14)

    plt.title("Figure 1. System Architecture of the AI-Assisted Decision-Support Prototype", fontsize=11)

    st.pyplot(fig)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Export Architecture Figure (PNG)"):
            fig.savefig(export_path, dpi=300, bbox_inches="tight")
            st.success(f"Exported: {export_path.as_posix()}")
    with col2:
        st.caption("Tip: Use this PNG directly as Figure 1 in your IEEE paper.")

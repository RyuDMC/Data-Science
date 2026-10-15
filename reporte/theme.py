"""
Tema visual y helpers de gráficos Matplotlib para el reporte.
Paleta consistente por propulsión, estilo limpio, una idea por gráfico.
"""

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from typing import Optional, List, Dict, Any


# ==================== PALETA POR PROPULSIÓN ====================
PROP_COLORS = {
    "electrico": "#1f77b4",   # azul
    "hibrido": "#ff7f0e",     # naranja
    "gasolina": "#d62728",    # rojo
    "indeterminado": "#7f7f7f",
}

PROP_LABELS = {
    "electrico": "Eléctrico",
    "hibrido": "Híbrido",
    "gasolina": "Gasolina",
    "indeterminado": "Indeterminado",
}

# Colores para resaltar vs fondo
HIGHLIGHT = "#1f77b4"
MUTED = "#b0b0b0"
GRID_COLOR = "#dddddd"
TEXT_COLOR = "#333333"
ACCENT_GREEN = "#2ca02c"
ACCENT_RED = "#d62728"


# ==================== ESTILO BASE ====================
def apply_style():
    """Aplica estilo global a Matplotlib."""
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": GRID_COLOR,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID_COLOR,
        "grid.linewidth": 0.8,
        "grid.alpha": 0.6,
        "axes.axisbelow": True,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlecolor": TEXT_COLOR,
        "axes.labelsize": 11,
        "axes.labelcolor": TEXT_COLOR,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    })


def color_for_prop(prop: str) -> str:
    """Devuelve color para una propulsión."""
    return PROP_COLORS.get(prop.lower() if prop else "indeterminado", PROP_COLORS["indeterminado"])


def label_for_prop(prop: str) -> str:
    """Devuelve etiqueta legible para propulsión."""
    return PROP_LABELS.get(prop.lower() if prop else "indeterminado", "Indeterminado")


# ==================== HELPERS DE GRÁFICOS ====================

def fig_ax(figsize=(10, 6), **kwargs):
    """Crea figura y ejes con estilo aplicado.

    Acepta los mismos kwargs que ``plt.subplots`` (p. ej. ``subplot_kw``
    para gráficos polares/radar).
    """
    apply_style()
    fig, ax = plt.subplots(figsize=figsize, **kwargs)
    return fig, ax


def save_fig(fig, path: str):
    """Guarda figura y cierra."""
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)


def bar_ranking(ax, models: List[str], scores: List[float], props: List[str],
                highlight_idx: Optional[int] = None,
                xlabel: str = "Score (0-1)", title: str = ""):
    """
    Barras horizontales de ranking.
    - models, scores, props: listas paralelas
    - highlight_idx: índice a resaltar (color propulsión, resto gris)
    """
    y = np.arange(len(models))
    colors = [color_for_prop(p) for p in props]
    if highlight_idx is not None:
        colors = [MUTED if i != highlight_idx else colors[i] for i in range(len(models))]

    bars = ax.barh(y, scores, color=colors, edgecolor="white", height=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(models, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_xlim(0, max(1.0, max(scores) * 1.15))
    ax.set_title(title, pad=12)

    # Valores en barras
    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f"{score:.3f}", va="center", fontsize=8, color=TEXT_COLOR)

    # Leyenda de propulsión
    from matplotlib.patches import Patch
    seen = set()
    handles = []
    for p in props:
        if p not in seen:
            handles.append(Patch(color=color_for_prop(p), label=label_for_prop(p)))
            seen.add(p)
    ax.legend(handles=handles, loc="lower right", fontsize=9)


def scatter_bubble(ax, x: np.ndarray, y: np.ndarray, size: np.ndarray,
                   props: List[str], labels: List[str],
                   highlight_idx: Optional[int] = None,
                   xlabel: str = "", ylabel: str = "", title: str = "",
                   xlog: bool = False, ylog: bool = False):
    """
    Scatter con burbujas (size = carga_kg o similar).
    - highlight_idx: resaltar uno
    """
    colors = [color_for_prop(p) for p in props]
    alphas = [0.9 if i == highlight_idx else 0.6 for i in range(len(x))]
    sizes = np.clip(size / size.max() * 800 + 50, 50, 1000) if len(size) > 0 else [100]

    for i in range(len(x)):
        ax.scatter(x[i], y[i], s=sizes[i], c=colors[i], alpha=alphas[i],
                   edgecolors="white", linewidth=0.5, zorder=3)
        if i == highlight_idx or len(x) < 15:
            ax.annotate(labels[i], (x[i], y[i]), fontsize=8, ha="center", va="bottom",
                        xytext=(0, 5), textcoords="offset points", color=TEXT_COLOR)

    if xlog: ax.set_xscale("log")
    if ylog: ax.set_yscale("log")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=12)

    # Leyenda propulsión
    from matplotlib.patches import Patch
    seen = set()
    handles = []
    for p in props:
        if p not in seen:
            handles.append(Patch(color=color_for_prop(p), label=label_for_prop(p)))
            seen.add(p)
    if handles:
        ax.legend(handles=handles, loc="upper left", fontsize=9)


def radar_chart(ax, categories: List[str], values_dict: Dict[str, List[float]],
                title: str = ""):
    """
    Radar chart comparando varios modelos.
    values_dict: {model_name: [val0..valN]} (valores 0-1)
    """
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # cerrar

    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=7)
    ax.grid(color=GRID_COLOR, linewidth=0.8)

    for (name, vals), prop in zip(values_dict.items(), [None]*len(values_dict)):
        # Inferir prop del nombre si está en el dict
        color = HIGHLIGHT  # default
        vals_closed = vals + vals[:1]
        ax.plot(angles, vals_closed, color=color, linewidth=2, label=name, zorder=3)
        ax.fill(angles, vals_closed, color=color, alpha=0.15)

    ax.set_title(title, pad=20, fontsize=12)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9)


def donut_chart(ax, values: List[float], labels: List[str], colors: List[str],
                title: str = ""):
    """Gráfico de dona."""
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors,
                                       autopct="%1.0f%%", startangle=90,
                                       pctdistance=0.75, wedgeprops=dict(width=0.45,
                                       edgecolor="white", linewidth=2))
    for t in texts: t.set_fontsize(9)
    for t in autotexts: t.set_fontsize(9); t.set_color("white"); t.set_fontweight("bold")
    ax.set_title(title, pad=12)
    ax.axis("equal")


def annotate_frontera(ax, x: np.ndarray, y: np.ndarray, labels: List[str],
                      props: List[str], xlabel: str, ylabel: str):
    """
    Dibuja la 'frontera eficiente' (Pareto) en un scatter precio vs autonomía/carga.
    """
    # Ordenar por x ascendente
    idx = np.argsort(x)
    x_s, y_s = x[idx], y[idx]

    # Frontera superior (max y para cada x o mayor)
    pareto_x, pareto_y, pareto_labels = [], [], []
    max_y = -1
    for xi, yi, li in zip(x_s, y_s, np.array(labels)[idx]):
        if yi > max_y:
            pareto_x.append(xi)
            pareto_y.append(yi)
            pareto_labels.append(li)
            max_y = yi

    ax.plot(pareto_x, pareto_y, color=ACCENT_GREEN, linestyle="--", linewidth=2,
            label="Frontera eficiente", zorder=4)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def table_mpl(ax, df, columns: List[str], title: str = "", max_rows: int = 15):
    """Renderiza un DataFrame como tabla en Matplotlib."""
    df_show = df[columns].head(max_rows).copy()
    # Formatear numéricos
    for col in df_show.columns:
        if df_show[col].dtype in ("float64", "float32"):
            df_show[col] = df_show[col].apply(lambda v: f"{v:.3f}" if pd.notna(v) else "—")
        elif df_show[col].dtype in ("int64", "int32"):
            df_show[col] = df_show[col].apply(lambda v: f"{v:,}" if pd.notna(v) else "—")

    ax.axis("off")
    table = ax.table(cellText=df_show.values,
                     colLabels=[c.replace("_", " ").title() for c in df_show.columns],
                     loc="center", cellLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor("#f0f2f6")
            cell.set_text_props(fontweight="bold")
        else:
            cell.set_facecolor("white" if r % 2 == 0 else "#fafafa")
    ax.set_title(title, pad=12, fontsize=12)


import pandas as pd  # para table_mpl
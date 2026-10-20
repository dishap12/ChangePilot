"""Charts for the fictional requirements demo; charts never infer dependencies."""
from __future__ import annotations
from collections import Counter

import plotly.graph_objects as go
from .models import Change, TraceLink
from .traceability import linked_items

COLORS = {
    "Added": "#1D8A7B",
    "Modified": "#5865DD",
    "Removed": "#E07A48",
    "Unchanged": "#BCC5D5",
}


def change_donut(changes: list[Change]) -> go.Figure:
    counts = Counter(item.status for item in changes)
    labels = [status for status in COLORS if counts[status]]
    values = [counts[status] for status in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=.70, sort=False,
        marker=dict(colors=[COLORS[x] for x in labels]),
        textinfo="none", hovertemplate="%{label}: %{value} requirements<extra></extra>",
    ))
    fig.update_layout(
        height=298, margin=dict(l=10, r=10, t=8, b=8), showlegend=True,
        legend=dict(orientation="h", y=-0.10, x=0, font=dict(size=12)),
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>{len(changes)}</b><br><span style='font-size:12px'>requirements</span>",
                          x=.5, y=.52, showarrow=False, font=dict(size=25, color="#192744"))],
    )
    return fig


def dependency_sankey(change: Change, links: list[TraceLink]) -> go.Figure | None:
    """Requirement -> system -> owner/test; only CSV-supplied links are graphed."""
    linked = linked_items(change.id, links)
    if not linked:
        return None
    identifiers: dict[tuple[str, str], int] = {}
    names, colors, origins, targets, edges = [], [], [], [], set()
    palette = {"requirement": "#5865DD", "system": "#3F8BC0",
               "owner": "#1D8A7B", "test": "#E3A65B"}

    def node(kind: str, name: str) -> int:
        key = (kind, name)
        if key not in identifiers:
            identifiers[key] = len(names)
            names.append(name)
            colors.append(palette[kind])
        return identifiers[key]

    source_req = node("requirement", change.id)
    for item in linked:
        if not item.system.strip():
            continue
        system = node("system", item.system)
        edges.add((source_req, system))
        if item.owner.strip():
            edges.add((system, node("owner", f"Owner: {item.owner}")))
        if item.test_case.strip():
            edges.add((system, node("test", f"Test: {item.test_case}")))
    if not edges:
        return None
    for a, b in sorted(edges):
        origins.append(a)
        targets.append(b)
    fig = go.Figure(go.Sankey(
        arrangement="snap", node=dict(pad=22, thickness=20, line=dict(color="#ffffff", width=1.5),
                                      label=names, color=colors,
                                      hovertemplate="%{label}<extra>Mapped from CSV</extra>"),
        link=dict(source=origins, target=targets, value=[1]*len(origins),
                  color="rgba(88, 101, 221, 0.20)", hovertemplate="Verified mapping<extra></extra>"),
    ))
    fig.update_layout(
        height=max(300, 55*len(linked)+200), margin=dict(l=18, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(size=12, color="#273650"),
    )
    return fig

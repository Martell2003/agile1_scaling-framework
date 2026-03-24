import streamlit as st
import plotly.graph_objects as go

st.title("Results Dashboard")
st.markdown("---")

results = st.session_state.get("results")
profile = st.session_state.get("profile")
rationale = st.session_state.get("rationale")

if not results:
    st.warning("No results to display yet. Please complete the Organisational Assessment first.")
    st.stop()

# --- Ranked recommendation ---
top = results[0]["framework"]
st.subheader(f"Recommended Framework: {top}")
st.info(rationale)
st.markdown("---")

# --- Bar chart ---
names = [r["framework"] for r in results]
scores = [r["score"] for r in results]
colors = ["#2E75B6" if i == 0 else "#A9C4E2" for i in range(len(names))]

bar_fig = go.Figure(go.Bar(
    x=names,
    y=scores,
    marker_color=colors,
    text=[str(s) for s in scores],
    textposition="outside"
))
bar_fig.update_layout(
    title="Framework Scores",
    yaxis=dict(range=[0, 1], title="Composite Score"),
    xaxis_title="Framework",
    height=400
)
st.plotly_chart(bar_fig, use_container_width=True)

# --- Radar chart ---
dimensions = [
    "cultural_maturity",
    "regulatory_constraint",
    "technical_debt",
    "organizational_size",
    "governance_model",
    "team_distribution",
    "sector_fit"
]

from data_access import load_framework_data
frameworks_data = load_framework_data()
sector = profile["sector"]

radar_fig = go.Figure()

colors_radar = {"SAFe": "#2E75B6", "LeSS": "#E05A2B", "Scrum@Scale": "#2E8B57"}

for fw_name, fw_scores in frameworks_data.items():
    fw_flat = dict(fw_scores)
    fw_flat["sector_fit"] = fw_scores["sector_fit"][sector]
    values = [fw_flat[d] for d in dimensions]
    values.append(values[0])  # close the radar shape

    radar_fig.add_trace(go.Scatterpolar(
        r=values,
        theta=dimensions + [dimensions[0]],
        fill="toself",
        name=fw_name,
        line_color=colors_radar[fw_name],
        opacity=0.6
    ))

radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    title="Framework Comparison — All Dimensions",
    height=500
)
st.plotly_chart(radar_fig, use_container_width=True)

# --- Raw scores table ---
st.markdown("---")
st.subheader("Score Breakdown")
for r in results:
    st.metric(label=r["framework"], value=r["score"])
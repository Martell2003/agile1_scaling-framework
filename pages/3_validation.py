import streamlit as st
from validator import load_checklist, save_feedback, get_validation_summary

st.title("Expert Validation Interface")
st.markdown("This page is for the MSc Programme Leader to assess the tool's logic, weights, and usability.")
st.markdown("---")

# --- Current validation status ---
summary = get_validation_summary()

if summary["total_sessions"] > 0:
    st.success(
        f"**{summary['total_sessions']} validation session(s) recorded.** "
        f"Latest: {summary['latest_timestamp']}"
    )
    with st.expander("View latest session summary"):
        latest = summary["latest_summary"]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", latest["total_items"])
        with col2:
            st.metric("Passed", latest["passed"])
        with col3:
            st.metric("Failed", latest["failed"])
        if summary["latest_comments"]:
            st.markdown("**Comments:**")
            st.write(summary["latest_comments"])
else:
    st.info("No validation sessions recorded yet.")

st.markdown("---")

# --- Checklist form ---
st.subheader("Validation Checklist")
st.markdown("Review each item and mark it as Pass or Fail based on your assessment of the tool.")

checklist = load_checklist()
responses = {}

for item in checklist:
    responses[item] = st.radio(
        item,
        ["Pass", "Fail"],
        horizontal=True,
        key=item
    )

st.markdown("---")

# --- Case study verification ---
st.subheader("Simulated Case Testing")
st.markdown("The table below shows the three case studies used to verify tool recommendations.")

from data_access import load_case_studies
cases = load_case_studies()

for case in cases:
    with st.expander(f"{case.get('id', 'N/A')} — {case.get('organisation', 'N/A')}"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Sector:** {case.get('sector', 'N/A')}")
            st.markdown(f"**Size:** {case.get('org_size', 'N/A')} employees")
            st.markdown(f"**Governance:** {case.get('governance_model', 'N/A')}")
            st.markdown(f"**Cultural Maturity:** {case.get('cultural_maturity', 'N/A')}/5")
        with col2:
            st.markdown(f"**Regulatory Constraint:** {case.get('regulatory_constraint', 'N/A')}/5")
            st.markdown(f"**Technical Debt:** {case.get('technical_debt', 'N/A')}/5")
            st.markdown(f"**Actual Framework:** {case.get('actual_framework_adopted', 'N/A')}")
            st.markdown(f"**Outcome:** {case.get('transformation_outcome', 'N/A')}")
        st.markdown(f"**Notes:** {case.get('notes', 'N/A')}")

st.markdown("---")

# --- Comments and submission ---
st.subheader("Additional Comments")
comments = st.text_area(
    "Provide any additional feedback on the tool's logic, usability, or recommendations.",
    height=150
)

if st.button("Submit Validation", type="primary"):
    if not comments.strip():
        st.warning("Please add at least a brief comment before submitting.")
    else:
        save_feedback(responses, comments)
        st.session_state["validated"] = True
        st.success("Validation record saved. Thank you for completing the review.")
        st.balloons()
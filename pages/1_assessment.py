import streamlit as st
from input_processor import validate_inputs
from saw_engine import calculate_scores, generate_rationale

st.title("Organisational Assessment")
st.markdown("Enter your organisation's profile below and click **Run Analysis**.")
st.markdown("---")

sector = st.selectbox("Sector", ["Technology", "Government"])
org_size = st.number_input("Organisation Size (number of employees)", min_value=1, value=500)
governance = st.selectbox("Governance Model", ["Centralized", "Devolved", "Hybrid"])
maturity = st.slider("Cultural Maturity", min_value=1, max_value=5, value=3,
                     help="1 = Low agile maturity, 5 = High agile maturity")
regulation = st.slider("Regulatory Constraint", min_value=1, max_value=5, value=3,
                       help="1 = Low regulatory pressure, 5 = High regulatory pressure")
debt = st.slider("Technical Debt", min_value=1, max_value=5, value=3,
                 help="1 = Low technical debt, 5 = High technical debt")

st.markdown("---")

if st.button("Run Analysis", type="primary"):
    profile = {
        "sector": sector,
        "org_size": org_size,
        "governance_model": governance,
        "cultural_maturity": maturity,
        "regulatory_constraint": regulation,
        "technical_debt": debt
    }

    valid, message = validate_inputs(profile)

    if not valid:
        st.error(f"Input error: {message}")
    else:
        results = calculate_scores(profile)
        rationale = generate_rationale(profile, results)

        st.session_state["profile"] = profile
        st.session_state["results"] = results
        st.session_state["rationale"] = rationale

        st.success("Analysis complete. Navigate to **Results Dashboard** in the sidebar.")
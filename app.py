import streamlit as st

st.set_page_config(
    page_title="Agile Scaling DSS",
    page_icon="🔄",
    layout="wide"
)

# Initialise session state on first load
if "results" not in st.session_state:
    st.session_state["results"] = None

if "profile" not in st.session_state:
    st.session_state["profile"] = {}

if "validated" not in st.session_state:
    st.session_state["validated"] = False

# Home page content
st.title("Agile Scaling Framework Decision Support Tool")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Step 1**\n\nGo to **Assessment** in the sidebar and enter your organisation's profile.")

with col2:
    st.success("**Step 2**\n\nClick **Run Analysis** to score your profile against SAFe, LeSS, and Scrum@Scale.")

with col3:
    st.warning("**Step 3**\n\nView your ranked recommendations and rationale on the **Results Dashboard**.")

st.markdown("---")

# Status indicators
st.subheader("Session Status")

col4, col5 = st.columns(2)

with col4:
    if st.session_state["results"]:
        st.success("Analysis complete — results are ready.")
    else:
        st.warning("No analysis run yet — complete the Assessment first.")

with col5:
    if st.session_state["validated"]:
        st.success("Expert validation submitted.")
    else:
        st.info("Expert validation not yet completed.")
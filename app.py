import streamlit as st
import pandas as pd

from rag import create_vector_store, retrieve_context
from agent import run_agent, create_plot, memory
from guardrails import is_safe_prompt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
.metric {
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("## 🚀 AI Data Analyst Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📂 Upload Data")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# ---------------- MAIN ----------------
if file:
    df = pd.read_csv(file)

    # -------- FILTER --------
    st.sidebar.header("🔎 Filters")

    selected_column = st.sidebar.selectbox(
        "Choose column to filter",
        df.columns
    )

    selected_values = st.sidebar.multiselect(
        f"Select {selected_column}",
        df[selected_column].unique(),
        default=df[selected_column].unique()
    )

    df = df[df[selected_column].isin(selected_values)]

    # -------- KPI CARDS --------
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    # Dynamic KPIs (works for any dataset)
    if "Sales" in df.columns:
        col1.metric("Total Sales", int(df["Sales"].sum()))
    else:
        col1.metric("Rows", len(df))

    if "Profit" in df.columns:
        col2.metric("Total Profit", int(df["Profit"].sum()))
    elif "CSAT_Score" in df.columns:
        col2.metric("Avg CSAT", round(df["CSAT_Score"].mean(), 2))
    else:
        col2.metric("Columns", len(df.columns))

    if "Orders" in df.columns:
        col3.metric("Total Orders", int(df["Orders"].sum()))
    elif "DSAT_Flag" in df.columns:
        col3.metric("DSAT %", round((df["DSAT_Flag"] == "Yes").mean() * 100, 2))
    else:
        col3.metric("Unique Values", df.nunique().sum())

    # -------- CHARTS --------
    st.markdown("### 📈 Visualizations")
    c1, c2 = st.columns(2)

    # Chart 1 (dynamic)
    with c1:
        st.subheader("Trend")

        if "Month" in df.columns and "Sales" in df.columns:
            st.line_chart(df.set_index("Month")["Sales"])
        else:
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) > 0:
                st.line_chart(df[numeric_cols])

    # Chart 2 (dynamic)
    with c2:
        st.subheader("Comparison")

        if "Category" in df.columns and "Profit" in df.columns:
            st.bar_chart(df.groupby("Category")["Profit"].sum())
        else:
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) > 0:
                st.bar_chart(df[numeric_cols].sum())

    # -------- DATA --------
    st.markdown("### 📄 Data Preview")
    st.dataframe(df)

    # -------- AI SECTION --------
    st.markdown("### 🤖 Ask AI")

    if "vs" not in st.session_state:
        st.session_state.vs = create_vector_store(df)

    query = st.text_input("Ask your question")

    if query:
        if not is_safe_prompt(query):
            st.error("Unsafe query!")
        else:
            context = retrieve_context(st.session_state.vs, query)
            response = run_agent(df, query, context)

            st.success(response)

            if "plot" in response.lower():
                create_plot(df)
                st.image("plot.png")

    # -------- MEMORY --------
    st.markdown("### 🧠 Memory")
    for role, msg in memory:
        st.write(f"{role}: {msg}")

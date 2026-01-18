import streamlit as st
import pandas as pd
from config import HISTORICAL_DATA_PATH, PROJECT_DIR
import altair as alt

@st.cache_data
def load_data():
    """Load historical data with caching."""
    try:
        if HISTORICAL_DATA_PATH.exists():
            return pd.read_csv(HISTORICAL_DATA_PATH)
        else:
            st.error(f"Data file not found: {HISTORICAL_DATA_PATH}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def explore_page():
    """Data exploration and visualization page."""
    st.title("📊 Data Explorer")
    st.markdown("Analyze historical medicine prescription data")
    
    df = load_data()
    
    if df.empty:
        st.warning("No data available to explore")
        return
    
    # Statistics section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Unique Medicines", df['Medicine'].nunique() if 'Medicine' in df.columns else 0)
    with col3:
        avg_qty = df['Quantity'].mean() if 'Quantity' in df.columns else 0
        st.metric("Avg Quantity", f"{avg_qty:.0f} mg")
    with col4:
        max_qty = df['Quantity'].max() if 'Quantity' in df.columns else 0
        st.metric("Max Quantity", f"{max_qty:.0f} mg")
    
    st.divider()
    
    # Filters
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        if 'Medicine' in df.columns:
            selected_medicines = st.multiselect(
                "Filter by Medicine",
                df['Medicine'].unique(),
                default=df['Medicine'].unique()[:3]
            )
        else:
            selected_medicines = []
    
    with col_filter2:
        chart_type = st.selectbox(
            "Chart Type",
            ["Bar Chart", "Line Chart", "Box Plot", "Scatter Plot"]
        )
    
    # Filter data
    if selected_medicines and 'Medicine' in df.columns:
        filtered_df = df[df['Medicine'].isin(selected_medicines)]
    else:
        filtered_df = df
    
    # Create visualizations
    st.subheader("Visualization")
    
    if not filtered_df.empty and 'Medicine' in filtered_df.columns and 'Quantity' in filtered_df.columns:
        try:
            if chart_type == "Bar Chart":
                chart = alt.Chart(filtered_df).mark_bar().encode(
                    x='Medicine:N',
                    y='mean(Quantity):Q'
                )
            elif chart_type == "Line Chart":
                chart = alt.Chart(filtered_df).mark_line().encode(
                    x='Medicine:N',
                    y='mean(Quantity):Q'
                )
            elif chart_type == "Box Plot":
                chart = alt.Chart(filtered_df).mark_boxplot().encode(
                    x='Medicine:N',
                    y='Quantity:Q'
                )
            else:  # Scatter Plot
                chart = alt.Chart(filtered_df).mark_point().encode(
                    x='Medicine:N',
                    y='Quantity:Q'
                )
            
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Visualization error: {e}")
    else:
        st.info("Select at least one medicine to visualize")
    
    st.divider()
    
    # Data table
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)
